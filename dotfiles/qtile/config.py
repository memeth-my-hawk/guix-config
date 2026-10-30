import os
from collections.abc import Callable

import subprocess
from libqtile import hook

import libqtile.resources
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
#from libqtile.utils import guess_terminal
from libqtile.config import Key


@hook.subscribe.startup_once
def autostart():
    commands = [
        # Display and Scaling
        #"xrandr --output HDMI-2 --mode 1920x1080 --rate 120.00 --left-of eDP-1 --output eDP-1 --mode 1920x1080 --rate 60.00",
        # "echo 'Xft.dpi: 96' | xrdb -merge",

        # Disable screen blanking, screen savers, and DPMS completely
        "xset s off",
        "xset -dpms",
        "xset s noblank",

        # Authentication Agent
        "/run/current-system/profile/libexec/polkit-gnome-authentication-agent-1",

        # System Tray Applets
        "nm-applet",
        "blueman-applet",
        "udiskie -t",

        # Screen Locking (xss-lock will still listen, but xset won't trigger blanks automatically)
        "xss-lock -- xlock",

        # Touchpad Management
        "syndaemon -i 0.5 -t -K -R -d"
    ]

    for cmd in commands:
        subprocess.Popen(cmd, shell=True)


@hook.subscribe.screen_change
def restart_on_screen_change(qtile):
    # This triggers autorandr to apply the correct profile instantly on plug/unplug
    subprocess.call(["autorandr", "--change"])


mod = "mod4"
alt = "mod1"
terminal = "alacritty"
editor = "emacsclient -c -a 'emacs'"

# Solarized Light with Orange Accent Palette
colors = {
    "bg": "#fdf6e3",       # Creamy white background
    "fg": "#657b83",       # Default text color (dark grey/blue)
    "accent": "#cb4b16",   # Orange accent for active elements
    "inactive": "#eee8d5", # Muted background for inactive workspaces
    "urgent": "#dc322f"    # Red for urgent notifications
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "m", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "e", lazy.spawn(editor), desc="Launch Emacs client"),


# --- Audio Controls (PulseAudio) ---
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioMicMute", lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle")),

    # --- Backlight Controls (brightnessctl) ---
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),

    # --- Screenshots (maim + xclip) ---
    # Fullscreen to ~/Pictures
    Key([], "Print", 
	lazy.spawn("sh -c 'maim | tee ~/pictures/screenshot_$(date +%s).png | xclip -selection clipboard -t image/png'"), 
	desc="Full screenshot to file and clipboard"),
    # Selection directly to clipboard
    Key(["shift"], "Print", 
    	lazy.spawn("sh -c 'maim -s | tee ~/pictures/screenshot_$(date +%s).png | xclip -selection clipboard -t image/png'"), 
    	desc="Partial screenshot to file and clipboard"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# --- Layouts ---
layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors["accent"],
    "border_normal": colors["inactive"],
    "single_border_width": 0,
    "single_margin": 0,
}

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


# --- Widget Typography ---
widget_defaults = dict(
    font="Source Code Pro",
    fontsize=14,
    padding=4,
    background=colors["bg"],
    foreground=colors["fg"],
)

extension_defaults = widget_defaults.copy()

logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")


screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="line",
                    this_current_screen_border=colors["accent"],
                    active=colors["fg"],
                    inactive=colors["inactive"],
                    highlight_color=colors["bg"],
                    urgent_border=colors["urgent"],
                    padding_x=6,
                    padding_y=3,
                    margin_x=0,
                    borderwidth=2,
                    disable_drag=True,
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["inactive"]),
                widget.Prompt(
                    prompt="run > ",
                    foreground=colors["accent"],
                    cursor_color=colors["accent"],
                ),
                widget.WindowName(max_chars=45, foreground=colors["fg"]),


                widget.Systray(padding=6, icon_size=16),
                widget.Sep(linewidth=1, padding=10, foreground=colors["inactive"]),

		widget.TextBox(text="♪", foreground=colors["accent"]),
                widget.Volume(
                    foreground=colors["fg"],
                    step=5,
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["inactive"]),

		# RAM Usage
                widget.TextBox(text="RAM", foreground=colors["accent"]),
                widget.Memory(
                    format="{MemUsed: .0f}{mm}",
                    foreground=colors["fg"],
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["inactive"]),

                widget.TextBox(text="⚡", foreground=colors["accent"]),
                widget.Battery(
                    format="{percent:2.0%} {char}",
                    charge_char="(+)",
                    discharge_char="(-)",
                    full_char="(==)",
		    not_charging_char="(~)",
                    low_percentage=0.20,
                    low_foreground=colors["urgent"],
                    update_delay=15,
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["inactive"]),
                widget.Clock(format="%a, %b %d, %H:%M", foreground=colors["fg"]),
            ],
            26, # Slightly thicker bar to accommodate Source Code Pro
        ),
    ),
]


# Instead of screens, you can define a function here to specify which Screen
# should correspond to which Output.
fake_screens: list[Screen] | None = None

# Instead of screens or fake screens, you can define a function here that
# returns a list of Screen objects based on the list of Outputs; that way you
# can decide based on e.g. the number of screens, or which ports are plugged
# in exactly what do render in each bar for each screen.
generate_screens: Callable[[list[Output]], list[Screen]] | None = None

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],

    border_focus=colors["accent"],
    border_normal=colors["inactive"],
    border_width=2,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

idle_timers = []  # type: list
idle_inhibitors = []  # type: list

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
