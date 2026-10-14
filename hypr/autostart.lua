-------------------
---- AUTOSTART ----
-------------------

-- See https://wiki.hypr.land/configuring/core/autostart/

-- Autostart necessary processes (like notifications daemons, status bars, etc.)
-- Or execute your favorite apps at launch like this:
--
hl.on("hyprland.start", function ()
  -- Xresources, so urxvt looks nize
  hl.exec_cmd("xrdb $HOME/.Xresources")
--   hl.exec_cmd(terminal)
--   hl.exec_cmd("nm-applet")
  hl.exec_cmd("waybar & hyprpaper")
end)
