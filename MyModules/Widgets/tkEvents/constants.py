Type_Activate = '36'
# A widget is changing from being inactive to being active. This refers to changes
# in the state option of a widget such as a button changing from inactive(grayed out) to active.
Type_ButtonPress = '4'
# The user pressed one of the mouse buttons. The detail part specifies which button.
# For mouse wheel support under Linux, use Button-4 (scroll up) and Button-5 (scroll down).
# Under Linux, your handler for mouse wheel bindings will distinguish between scroll-up and scroll-down by
# examining the .num field of the Event instance
Type_ButtonRelease = '5'
# The user let up on a mouse button. This is probably a better choice in most cases than the Button event,
# because if the user accidentally presses the button, they can move the mouse off the widget to
# avoid setting off the event.
Type_Configure = '22'
# The user changed the size of a widget, for example by dragging a corner or side of the window.
Type_Deactivate = '37'
# Awidget is changing from being active to being inactive. This refers to changes in the state option
# of a widget such as a radiobutton changing from active to inactive (grayed out).
Type_Destroy = '17'
# A widget is being destroyed.
Type_Enter = '7'
# The user moved the mouse pointer into a visible part of a widget. (This is
# different than the enter key, which is a KeyPress event for a key whose name is actually 'return'.)
Type_Expose = '12'
# This event occurs whenever at least some part of your application or widget
# becomes visible after having been covered up by another window.
Type_FocusIn = '9'
# A widget got the input focus. This can happen either in response to a user event (like using the tab key to
# move focus between widgets) or programmatically (for example, your program calls the .focus_set() on a widget).
Type_FocusOut = '10'
# The input focus was moved out of a widget. As with FocusIn, the user can cause this event, or
# your program can cause it.
Type_KeyPress = '2'
# The user pressed a key on the keyboard. The detail part specifies which
# key. This keyword may be abbreviated Key.
Type_KeyRelease = '3'
# The user let up on a key.
Type_Leave = '8'
# The user moved the mouse pointer out of a widget.
Type_Map = '19'
# A widget is being mapped, that is, made visible in the application. This will
# happen, for example, when you call the widget's .grid() method.
Type_Motion = '6'
# The user moved the mouse pointer entirely within a widget.
Type_MouseWheel = '38'
# The user moved the mouse wheel up or down. At present, this binding works
# on Windows and MacOS, but not under Linux.
# For Windows and MacOS, the .delta field of the Event instance
# For Linux, use ButtonPress-4 and ButtonPress-5.
Type_Unmap = '18'
# A widget is being unmapped and is no longer visible. This happens, for example,
# when you use the widget's .grid_remove() method.
Type_Visibility = '15'
# Happens when at least some part of the application window becomes visible on the screen.

# Name_Activate = 'Activate'
# Name_ButtonPress = 'ButtonPress'
# Name_ButtonRelease = 'ButtonRelease'
# Name_Configure = 'Configure'
# Name_Deactivate = 'Deactivate'
# Name_Destroy = 'Destroy'
# Name_Enter = 'Enter'
# Name_Expose = 'Expose'
# Name_FocusIn = 'FocusIn'
# Name_FocusOut = 'FocusOut'
# Name_KeyPress = 'KeyPress'
# Name_KeyRelease = 'KeyRelease'
# Name_Leave = 'Leave'
# Name_Map = 'Map'
# Name_Motion = 'Motion'
# Name_MouseWheel = 'MouseWheel'
# Name_Unmap = 'Unmap'
# Name_Visibility = 'Visibility'

# The left-hand alt key
# KeySym_Alt_L = 'Alt_L'
# KeyCode_Alt_L = '64'
# KeySym_Num_Alt_L = '65513'
#
# The right-hand alt key
# KeySym_Alt_R = 'Alt_R'
# KeyCode_Alt_R = '113'
# KeySym_Num_Alt_R = '65514'
#
# BackSpace 22 65288 backspace
# Cancel 110 65387 break
# Caps_Lock 66 65549 CapsLock
# Control_L 37 65507 The left-hand control key
# Control_R 109 65508 The right-hand control key
# Delete 107 65535 Delete
# End 103 65367 end
# Escape 9 65307 esc
# Execute 111 65378 SysReq
# F1 67 65470 Function key F1
# F2 68 65471 Function key F2
# Fi 66+i 65469+i Function key Fi
# F12 96 65481 Function key F12
# Home 97 65360 home
# Insert 106 65379 insert
# Linefeed 54 106 Linefeed (control-J)
# KP_0 90 65438 0 on the keypad
# KP_1 87 65436 1 on the keypad
# KP_2 88 65433 2 on the keypad
# KP_3 89 65435 3 on the keypad
# KP_4 83 65430 4 on the keypad
# KP_5 84 65437 5 on the keypad
# KP_6 85 65432 6 on the keypad
# KP_7 79 65429 7 on the keypad
# KP_8 80 65431 8 on the keypad
# KP_9 81 65434 9 on the keypad
# KP_Add 86 65451 + on the keypad
# KP_Begin 84 65437 The center key (same key as 5) on the keypad
# KP_Decimal 91 65439 Decimal (.) on the keypad
# KP_Delete 91 65439 delete on the keypad
# KP_Divide 112 65455 / on the keypad
# KP_Down 88 65433 "down arrow" on the keypad
# KP_End 87 65436 end on the keypad
# KP_Enter 108 65421 enter on the keypad
# KP_Home 79 65429 home on the keypad
# KP_Insert 90 65438 insert on the keypad
# KP_Left 83 65430 "left arrow" on the keypad
# KP_Multiply 63 65450 "*" on the keypad
# KP_Next 89 65435 PageDown on the keypad
# KP_Prior 81 65434 PageUp on the keypad
# KP_Right 85 65432 "right arrow" on the keypad
# KP_Subtract 82 65453 - on the keypad
# KP_Up 80 65431 "up arrow" on the keypad
# Next 105 65366 PageDown
# Num_Lock 77 65407 NumLock
# Pause 110 65299 pause
# Print 111 65377 PrintScrn
# Prior 99 65365 PageUp
# The enter key (control-M). The name Enter refers to a
# mouse-related event, not a keypress

keysym_Return = 'Return'
keycode_Return = 36
keysym_num_Return = 65293

# Scroll_Lock 78 65300 ScrollLock
# Shift_L 50 65505 The left-hand shift key
# Shift_R 62 65506 The right-hand shift key
keysym_Tab = 'Tab'
keycode_Tab = 23
keysym_num_Tab = 65289

keysym_Up = 'Up'
keycode_Up = 98
keysym_num_Up = 65362

keysym_Left = 'Left'
keycode_Left = 100
keysym_num_Left = 65361

keysym_Right = 'Right'
keycode_Right = 102
keysym_num_Right = 65363

keysym_Down = 'Down'
keycode_Down = 104
keysym_num_Down = 65364

# check the following by masking event.state
Modifier_Shift = 0x0001
Modifier_Control = 0x0004
Modifier_Left_Mouse_Button = 0x0100
Modifier_Middle_Mouse_Button = 0x0200
Modifier_Right_Mouse_Button = 0x0400
