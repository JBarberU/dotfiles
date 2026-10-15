require "autostart"
require "bindings"
require "environment"
require "input"
require "monitors"
require "programs"
require "theme"
require "windowing"

require "misc/ff_extension"

-- Load this file only on hosts that have custom configs
if package.searchpath("per_host", package.path) then
    require("per_host")
end
