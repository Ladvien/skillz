# tree_optimizer.gd
# Screenshot capture and parameter application for PixyTree optimization
# Add this to your Godot project: res://scripts/tree_optimizer.gd

extends Node

signal screenshot_ready(paths: Array)
signal parameters_applied()

## Reference to PixyTree node (set in editor or via code)
@export var pixy_tree: Node3D

## Viewport used for capturing screenshots
@export var capture_viewport: SubViewport

## Camera used for captures
@export var capture_camera: Camera3D

## Directory for saving screenshots
var screenshot_dir: String = "user://optimization_screenshots/"

## Current iteration number
var current_iteration: int = 0

## Camera angle presets (will be configured based on tree size)
var camera_angles: Array[Dictionary] = []


func _ready() -> void:
	# Create screenshot directory
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(screenshot_dir))
	
	# Setup default camera angles
	_setup_default_camera_angles()


func _setup_default_camera_angles() -> void:
	"""Setup default camera positions for tree capture."""
	camera_angles = [
		{
			"name": "three_quarter_front",
			"position": Vector3(5, 3, 5),
			"look_at": Vector3(0, 2, 0),
		},
		{
			"name": "side",
			"position": Vector3(7, 2, 0),
			"look_at": Vector3(0, 2.5, 0),
		},
		{
			"name": "top_angled",
			"position": Vector3(0, 8, 4),
			"look_at": Vector3(0, 2, 0),
		},
	]


func configure_camera_for_tree(tree_height: float, tree_radius: float) -> void:
	"""Adjust camera positions based on tree dimensions."""
	var center_height = tree_height * 0.5
	var distance = max(tree_height, tree_radius * 4) * 1.5
	
	camera_angles = [
		{
			"name": "three_quarter_front",
			"position": Vector3(distance * 0.7, center_height + tree_height * 0.3, distance * 0.7),
			"look_at": Vector3(0, center_height, 0),
		},
		{
			"name": "side",
			"position": Vector3(distance, center_height * 0.8, 0),
			"look_at": Vector3(0, center_height, 0),
		},
		{
			"name": "top_angled",
			"position": Vector3(0, tree_height * 1.5, distance * 0.6),
			"look_at": Vector3(0, center_height * 0.8, 0),
		},
	]


func capture_screenshots() -> Array[String]:
	"""Capture tree from multiple angles. Returns array of file paths."""
	var paths: Array[String] = []
	
	if not capture_viewport or not capture_camera:
		push_error("capture_viewport or capture_camera not set")
		return paths
	
	for i in range(camera_angles.size()):
		var angle = camera_angles[i]
		
		# Position camera
		capture_camera.global_position = angle["position"]
		capture_camera.look_at(angle["look_at"])
		
		# Wait for render to complete
		await RenderingServer.frame_post_draw
		await get_tree().process_frame
		
		# Capture image
		var image = capture_viewport.get_texture().get_image()
		
		# Generate filename
		var filename = "iter_%04d_%s.png" % [current_iteration, angle["name"]]
		var path = screenshot_dir + filename
		
		# Save image
		var err = image.save_png(path)
		if err != OK:
			push_error("Failed to save screenshot: %s" % path)
			continue
		
		# Convert to global path for Python
		var global_path = ProjectSettings.globalize_path(path)
		paths.append(global_path)
		
		print("Saved screenshot: %s" % global_path)
	
	current_iteration += 1
	screenshot_ready.emit(paths)
	
	return paths


func apply_parameters(params: Dictionary) -> void:
	"""Apply parameter dictionary to PixyTree node."""
	if not pixy_tree:
		push_error("pixy_tree not set")
		return
	
	# Apply each parameter
	for key in params:
		if pixy_tree.has_method("set"):
			var property_list = pixy_tree.get_property_list()
			for prop in property_list:
				if prop["name"] == key:
					pixy_tree.set(key, params[key])
					break
	
	# Trigger tree regeneration
	if pixy_tree.has_method("regenerate"):
		pixy_tree.regenerate()
	elif pixy_tree.has_method("generate"):
		pixy_tree.generate()
	elif pixy_tree.has_method("rebuild"):
		pixy_tree.rebuild()
	
	# Wait for regeneration to complete
	await get_tree().process_frame
	await get_tree().process_frame
	
	# Adjust camera based on new tree size
	var height = params.get("trunk_height", 6.0)
	var radius = params.get("trunk_radius", 0.5)
	configure_camera_for_tree(height, radius)
	
	parameters_applied.emit()


func run_optimization_step(params: Dictionary) -> Array[String]:
	"""Single optimization step: apply params and capture screenshots."""
	await apply_parameters(params)
	return await capture_screenshots()


func get_current_parameters() -> Dictionary:
	"""Get current parameters from PixyTree node."""
	if not pixy_tree:
		return {}
	
	var params = {}
	var property_list = pixy_tree.get_property_list()
	
	for prop in property_list:
		if prop["usage"] & PROPERTY_USAGE_EDITOR:
			var value = pixy_tree.get(prop["name"])
			if value != null:
				params[prop["name"]] = value
	
	return params
