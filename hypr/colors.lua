---------------------
---- MY COLORS ----
---------------------

local M = {}

M.gruvbox_dark = {
    bg0_soft = "rgba(32302fff)",
    bg1 = "rgba(3c3836ff)",
    bg3 = "rgba(665c54ff)",
    fg0 = "rgba(fbf1c7ff)",
    fg1 = "rgba(ebdbb2ff)",
    gray_dark = "rgba(a89984ff)",
    purple_dark = "rgba(b16286ff)",
    purple_light = "rgba(d3869bff)",
    red_dark = "rgba(cc241dff)",
    red_light = "rgba(fb4934ff)",
    yellow_dark = "rgba(d79921ff)",
    yellow_light = "rgba(fabd2fff)",
    blue_dark = "rgba(458588ff)",
    blue_light = "rgba(83a598ff)",
    green_dark = "rgba(98971aff)",
    green_dark = "rgba(b8bb26ff)",
    aqua_dark = "rgba(689d6aff)",
    aqua_light = "rgba(8ec07cff)",
    orange_dark = "rgba(d65d0eff)",
    orange_light = "rgba(fe8019ff)",
}

M.border_color = {
    active_border = { colors = {M.gruvbox_dark.purple_light, M.gruvbox_dark.purple_dark}, angle = 45 },
    inactive_border = M.gruvbox_dark.bg2,
}

M.shadow_color = 0xee1a1a1a

return M
