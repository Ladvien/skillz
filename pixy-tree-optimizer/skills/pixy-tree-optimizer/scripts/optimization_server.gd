# optimization_server.gd
# Headless HTTP server for PixyTree optimization
# Run with: godot --headless --script res://scripts/optimization_server.gd
#
# Endpoints:
#   POST /capture         - Capture screenshots, returns {"paths": [...]}
#   POST /apply_params    - Apply parameters (JSON body), returns {"status": "ok"}
#   POST /apply_render_config - Apply render configuration
#   GET  /get_status      - Get current status
#   GET  /get_params      - Get current tree parameters
#   POST /shutdown        - Gracefully shutdown server

extends SceneTree

var server: TCPServer
var port: int = 8765
var optimizer: Node  # tree_optimizer.gd instance
var pixy_tree: Node3D
var viewport: SubViewport
var camera: Camera3D
var environment: WorldEnvironment

# Render configuration
var current_render_config: Dictionary = {}


func _init() -> void:
	# Parse command line arguments
	var args = OS.get_cmdline_args()
	for i in range(args.size()):
		if args[i] == "--port" and i + 1 < args.size():
			port = int(args[i + 1])
	
	# Setup scene
	_setup_scene()
	
	# Start HTTP server
	server = TCPServer.new()
	var err = server.listen(port)
	if err != OK:
		push_error("Failed to start server on port %d: %s" % [port, error_string(err)])
		quit(1)
		return
	
	print("PixyTree Optimization Server started on port %d" % port)
	print("Endpoints:")
	print("  POST /capture")
	print("  POST /apply_params")
	print("  POST /apply_render_config")
	print("  GET  /get_status")
	print("  GET  /get_params")
	print("  POST /shutdown")


func _setup_scene() -> void:
	"""Create the optimization scene programmatically."""
	# Create root node
	var root_node = Node3D.new()
	root_node.name = "OptimizationRoot"
	root.add_child(root_node)
	
	# Create SubViewport for rendering
	viewport = SubViewport.new()
	viewport.name = "CaptureViewport"
	viewport.size = Vector2i(640, 480)  # Default, will be configured
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.transparent_bg = false
	root_node.add_child(viewport)
	
	# Create camera
	camera = Camera3D.new()
	camera.name = "CaptureCamera"
	camera.position = Vector3(5, 3, 5)
	camera.look_at(Vector3(0, 2, 0))
	camera.fov = 45.0
	viewport.add_child(camera)
	
	# Create environment
	environment = WorldEnvironment.new()
	var env = Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.78, 0.86, 0.94)  # Light blue
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.7, 0.75, 0.8)
	env.ambient_light_energy = 0.5
	environment.environment = env
	viewport.add_child(environment)
	
	# Create directional light (key light)
	var key_light = DirectionalLight3D.new()
	key_light.name = "KeyLight"
	key_light.rotation_degrees = Vector3(-50, -45, 0)
	key_light.light_energy = 1.0
	key_light.light_color = Color(1.0, 0.98, 0.95)
	key_light.shadow_enabled = true
	viewport.add_child(key_light)
	
	# Create fill light
	var fill_light = DirectionalLight3D.new()
	fill_light.name = "FillLight"
	fill_light.rotation_degrees = Vector3(-30, 135, 0)
	fill_light.light_energy = 0.4
	fill_light.light_color = Color(0.8, 0.85, 1.0)
	fill_light.shadow_enabled = false
	viewport.add_child(fill_light)
	
	# Try to load PixyTree - update path as needed
	var pixy_tree_scene = load("res://addons/pixy_tree/scenes/pixy_tree.tscn")
	if pixy_tree_scene:
		pixy_tree = pixy_tree_scene.instantiate()
		pixy_tree.name = "PixyTree"
		viewport.add_child(pixy_tree)
		print("PixyTree loaded successfully")
	else:
		# Create placeholder Node3D
		pixy_tree = Node3D.new()
		pixy_tree.name = "PixyTree_Placeholder"
		viewport.add_child(pixy_tree)
		push_warning("Could not load PixyTree scene, using placeholder")
	
	# Create optimizer helper
	var optimizer_script = load("res://scripts/tree_optimizer.gd")
	if optimizer_script:
		optimizer = Node.new()
		optimizer.set_script(optimizer_script)
		optimizer.pixy_tree = pixy_tree
		optimizer.capture_viewport = viewport
		optimizer.capture_camera = camera
		root_node.add_child(optimizer)
	else:
		push_warning("Could not load tree_optimizer.gd")


func _process(_delta: float) -> bool:
	"""Process incoming HTTP connections."""
	if server.is_connection_available():
		var connection = server.take_connection()
		if connection:
			_handle_connection(connection)
	return false  # Keep running


func _handle_connection(peer: StreamPeerTCP) -> void:
	"""Handle an incoming HTTP connection."""
	# Wait for data
	peer.set_no_delay(true)
	
	# Read request (simple HTTP parsing)
	var request_data = ""
	var start_time = Time.get_ticks_msec()
	
	while peer.get_status() == StreamPeerTCP.STATUS_CONNECTED:
		if Time.get_ticks_msec() - start_time > 5000:
			break  # Timeout
		
		var available = peer.get_available_bytes()
		if available > 0:
			request_data += peer.get_string(available)
			if "\r\n\r\n" in request_data:
				break
		else:
			await root.create_timer(0.01).timeout
	
	if request_data.is_empty():
		peer.disconnect_from_host()
		return
	
	# Parse HTTP request
	var lines = request_data.split("\r\n")
	var request_line = lines[0].split(" ")
	var method = request_line[0] if request_line.size() > 0 else "GET"
	var path = request_line[1] if request_line.size() > 1 else "/"
	
	# Get body for POST requests
	var body = ""
	var body_start = request_data.find("\r\n\r\n")
	if body_start != -1:
		body = request_data.substr(body_start + 4)
	
	# Route request
	var response = _route_request(method, path, body)
	
	# Send response
	var http_response = "HTTP/1.1 200 OK\r\n"
	http_response += "Content-Type: application/json\r\n"
	http_response += "Content-Length: %d\r\n" % response.length()
	http_response += "Connection: close\r\n"
	http_response += "\r\n"
	http_response += response
	
	peer.put_data(http_response.to_utf8_buffer())
	peer.disconnect_from_host()


func _route_request(method: String, path: String, body: String) -> String:
	"""Route HTTP request to appropriate handler."""
	print("Request: %s %s" % [method, path])
	
	match path:
		"/capture":
			return await _handle_capture()
		"/apply_params":
			return _handle_apply_params(body)
		"/apply_render_config":
			return _handle_apply_render_config(body)
		"/get_status":
			return _handle_get_status()
		"/get_params":
			return _handle_get_params()
		"/shutdown":
			_handle_shutdown()
			return JSON.stringify({"status": "shutting_down"})
		_:
			return JSON.stringify({"error": "Unknown endpoint: " + path})


func _handle_capture() -> String:
	"""Handle screenshot capture request."""
	if not optimizer:
		return JSON.stringify({"error": "Optimizer not initialized"})
	
	var paths = await optimizer.capture_screenshots()
	return JSON.stringify({"paths": paths})


func _handle_apply_params(body: String) -> String:
	"""Handle parameter application request."""
	if body.is_empty():
		return JSON.stringify({"error": "Empty body"})
	
	var params = JSON.parse_string(body)
	if params == null:
		return JSON.stringify({"error": "Invalid JSON"})
	
	if not optimizer:
		return JSON.stringify({"error": "Optimizer not initialized"})
	
	await optimizer.apply_parameters(params)
	return JSON.stringify({"status": "ok"})


func _handle_apply_render_config(body: String) -> String:
	"""Handle render configuration request."""
	if body.is_empty():
		return JSON.stringify({"error": "Empty body"})
	
	var config = JSON.parse_string(body)
	if config == null:
		return JSON.stringify({"error": "Invalid JSON"})
	
	current_render_config = config
	
	# Apply viewport settings
	if config.has("viewport"):
		var vp = config["viewport"]
		viewport.size = Vector2i(vp.get("width", 640), vp.get("height", 480))
	
	# Apply camera settings
	if config.has("camera"):
		var cam = config["camera"]
		camera.fov = cam.get("fov", 45.0)
	
	# Apply background
	if config.has("background") and environment:
		var bg = config["background"]
		if bg.get("type") == "solid_color":
			environment.environment.background_mode = Environment.BG_COLOR
			var c = bg.get("color", [200, 220, 240])
			environment.environment.background_color = Color(c[0]/255.0, c[1]/255.0, c[2]/255.0)
	
	return JSON.stringify({"status": "ok"})


func _handle_get_status() -> String:
	"""Handle status request."""
	return JSON.stringify({
		"status": "running",
		"port": port,
		"pixy_tree_loaded": pixy_tree != null,
		"viewport_size": [viewport.size.x, viewport.size.y] if viewport else [0, 0],
		"iteration": optimizer.current_iteration if optimizer else 0,
	})


func _handle_get_params() -> String:
	"""Handle get parameters request."""
	if not optimizer:
		return JSON.stringify({"error": "Optimizer not initialized"})
	
	var params = optimizer.get_current_parameters()
	return JSON.stringify(params)


func _handle_shutdown() -> void:
	"""Handle shutdown request."""
	print("Shutting down...")
	await get_tree().create_timer(0.1).timeout
	quit(0)
