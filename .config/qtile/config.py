# Qtile config - ThinkPad T480
# ~/.config/qtile/config.py

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.dgroups import simple_key_binder
import subprocess
import os

# ---------------------------------------------------------------------------
# Core settings
# ---------------------------------------------------------------------------
mod = "mod4"
terminal = "alacritty"
browser = "firefox"
obsidian = "obsidian"
discord = "discord"

# ---------------------------------------------------------------------------
# Keybindings
# ---------------------------------------------------------------------------
keys = [
    # Window focus (vim-style)
    Key([mod], "h", lazy.layout.left(), desc="Focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Focus next window"),

    # Window movement
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Window resize
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset window sizes"),

    # Stack control
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle split/unsplit stack"),

    # ThinkPad T480 media keys
    # Audio (PulseAudio via pactl — more reliable on modern setups than amixer)
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMicMute", lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle")),

    # Brightness (T480 intel_backlight)
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),

    # Screenshots (requires scrot or maim)
    Key([], "Print", lazy.spawn("scrot '%Y-%m-%d_%H-%M-%S_$wx$h.png' -e 'mv $f ~/Pictures/screenshots/'")),
    Key([mod], "Print", lazy.spawn("scrot -s '%Y-%m-%d_%H-%M-%S_$wx$h.png' -e 'mv $f ~/Pictures/screenshots/'")),

    # Lock screen (ThinkPad Fn+L or manual)
    Key([mod, "control"], "l", lazy.spawn("i3lock -c 1D2330"), desc="Lock screen"),

    # App launchers
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Browser"),
    Key([mod], "o", lazy.spawn(obsidian), desc="Obsidian"),
    Key([mod], "d", lazy.spawn(discord), desc="Discord"),
    Key([mod], "p", lazy.spawn("rofi -show drun"), desc="App launcher"),

    # Layout / session
    Key([mod], "Tab", lazy.next_layout(), desc="Next layout"),
    Key([mod], "w", lazy.window.kill(), desc="Kill window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn command prompt"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
]

# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------
groups = [Group(str(i), layout="monadtall") for i in range(1, 10)]
groups.append(Group("0", layout="floating"))

dgroups_key_binder = simple_key_binder("mod4")
dgroups_app_rules = []

# ---------------------------------------------------------------------------
# Layouts
# ---------------------------------------------------------------------------
layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": "#e1acff",
    "border_normal": "#1D2330",
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Columns(
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        **layout_theme,
    ),
    layout.Floating(**layout_theme),
]

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
colours = {
    "green": "#3df310",
    "teal": "#40E0D0",
    "gold": "#f5c518",
    "red": "#df2b52",
    "bg": "#1D2330",
    "fg": "#fdfefe",
}

# ---------------------------------------------------------------------------
# Widgets & bar
# ---------------------------------------------------------------------------
widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=13,
    padding=4,
    background=colours["bg"],
)
extension_defaults = widget_defaults.copy()

def build_bar():
    """Build a bar suitable for the T480 (or an external monitor)."""
    return bar.Bar(
        [
            widget.CurrentLayout(foreground=colours["green"]),
            widget.GroupBox(
                foreground=colours["green"],
                highlight_method="line",
                highlight_color=[colours["bg"], colours["bg"]],
                this_current_screen_border=colours["green"],
            ),
            widget.Pomodoro(length_pomodori=52, length_short_break=17),
            widget.Prompt(),
            widget.WindowName(foreground=colours["green"]),
            widget.Chord(
                chords_colors={"launch": ("#ff0000", "#ffffff")},
                name_transform=lambda name: name.upper(),
            ),
            widget.Systray(),
            widget.Sep(padding=10),

            # Network — T480 uses wlp3s0 (Wi-Fi) / enp0s31f6 (Ethernet)
            # Adjust interface name if yours differs (check `ip link`)
            widget.Net(
                interface="wlp3s0",
                format="{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}",
                foreground=colours["green"],
            ),
            widget.Sep(padding=10),

            # System stats
            widget.TextBox("RAM:", foreground=colours["green"]),
            widget.Memory(
                format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
                foreground=colours["green"],
            ),
            widget.CPU(format="CPU:{load_percent}%", foreground=colours["green"]),
            widget.Sep(padding=10),

            # ThinkPad T480 dual-battery support
            # BAT0 = internal battery, BAT1 = external/swappable battery
            widget.TextBox("BAT0:", foreground=colours["teal"]),
            widget.Battery(
                battery="BAT0",
                format="{percent:2.0%} {char}",
                charge_char="⚡",
                discharge_char="🔋",
                low_percentage=0.15,
                low_foreground=colours["red"],
                foreground=colours["teal"],
            ),
            widget.TextBox("BAT1:", foreground=colours["teal"]),
            widget.Battery(
                battery="BAT1",
                format="{percent:2.0%} {char}",
                charge_char="⚡",
                discharge_char="🔋",
                low_percentage=0.15,
                low_foreground=colours["red"],
                foreground=colours["teal"],
            ),
            widget.Sep(padding=10),

            # Backlight — T480 uses intel_backlight
            widget.TextBox("BRT:", foreground=colours["teal"]),
            widget.Backlight(
                backlight_name="intel_backlight",
                format="{percent:2.0%}",
                foreground=colours["teal"],
            ),

            # Volume
            widget.TextBox("VOL:", foreground=colours["teal"]),
            widget.Volume(
                foreground=colours["teal"],
                volume_app="pactl",
                update_interval=0.2,
            ),
            widget.Sep(padding=10),

            widget.Clock(
                format="%Y-%m-%d %a %I:%M %p",
                foreground=colours["gold"],
            ),
            widget.QuickExit(foreground=colours["red"]),
        ],
        26,
    )

# Primary screen (T480 built-in 14" display)
# Second screen entry for an external monitor — remove if single-screen only
screens = [
    Screen(
        top=build_bar(),
        wallpaper="~/.dotfiles/background.png",
        wallpaper_mode="stretch",
    ),
    Screen(
        top=build_bar(),
        wallpaper="~/.dotfiles/background.png",
        wallpaper_mode="stretch",
    ),
]

# ---------------------------------------------------------------------------
# Mouse / floating
# ---------------------------------------------------------------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

floating_layout = layout.Floating(
    border_focus=colours["teal"],
    border_normal=colours["bg"],
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
)

# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------
@hook.subscribe.startup_once
def autostart():
    """Run once on first login — add your startup apps here."""
    subprocess.Popen(["nm-applet"])         # NetworkManager tray
    subprocess.Popen(["blueman-applet"])    # Bluetooth tray

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["picom", "-b"])       # compositor for transparency
    subprocess.Popen(["nm-applet"])
    subprocess.Popen(["blueman-applet"])


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
