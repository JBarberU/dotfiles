---------------------
---- MY PROGRAMS ----
---------------------

-- Set programs that you use
local M = {}
M.terminal    = "urxvt"
M.fileManager = "nautilus"
M.menu        = "rofi -show combi -combi-modi \"run,drun\" -modi combi -matching fuzzy"
M.browser     = "firefox"
M.lock        = "hyprlock"

M.screenshot = {
    all_windows = "grim \"$(xdg-user-dir PICTURES)/screenshots/screenshot_$(date +%Y-%m-%d_%H-%M-%S).png\"",
    rectangle = "grim -g \"$(slurp -d)\" \"$(xdg-user-dir PICTURES)/screenshots/screenshot_$(date +%Y-%m-%d_%H-%M-%S).png\"",
}

return M
