// get player input
var keyLeft = keyboard_check(vk_left) || keyboard_check(ord("Q"));
var keyRight = keyboard_check(vk_right) || keyboard_check(ord("D"));
var keyUp = keyboard_check(vk_up) || keyboard_check(ord("Z"));
var keyDown = keyboard_check(vk_down) || keyboard_check(ord("S"));

// calculate angle and movement
var inputDirection = point_direction(0,0,keyRight-keyLeft,keyDown-keyUp)
var inputMagnitude = (keyRight-keyLeft != 0) or (keyDown-keyUp != 0);

hSpeed = lengthdir_x(inputMagnitude*speedWalk, inputDirection);
vSpeed = lengthdir_y(inputMagnitude*speedWalk, inputDirection);

// movement
x += hSpeed;
y += vSpeed;