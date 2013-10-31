import XMonad
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Layout.Fullscreen
import XMonad.Layout.NoBorders
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig(additionalKeys)
import System.IO
import Data.Ratio ((%))
import XMonad.Hooks.SetWMName
import qualified Data.Map as M
import qualified XMonad.StackSet as W
import System.Exit

myTerminal = "gnome-terminal"

myModMask = mod4Mask -- Rebind Mod to the windows key

myBorderWidth = 2

myNormalBorderColor = "black"

myFocusedBorderColor = "purple"

myFocusFollowsMouse = False

myWorkspaces = ["1. vim","2. term","3. web"] ++ map show [4..9]

myKeys conf@(XConfig {XMonad.modMask = modm}) = M.fromList $
	-- Launch a terminal
	[ ((modm .|. shiftMask, xK_Return), spawn $ XMonad.terminal conf)
	
	-- Launch dmenu (all)
    , ((modm .|. shiftMask,		xK_space ), spawn "exe=`dmenu_path | dmenu -b ` && eval \"exec $exe\"")
    , ((modm,					xK_space ), spawn "exe=`cat ~/.dmenu_favourites | dmenu -b ` && eval \"exec $exe\"")

	-- Launch nvidia-settings
	, ((modm .|. shiftMask, xK_n), spawn "nvidia-settings")

	-- Audio controls
	, ((0, 0x1008ff11), spawn "amixer -q set Master 10%-")
	, ((shiftMask, 0x1008ff11), spawn "amixer -q set Master 1%-")
	, ((0, 0x1008ff13), spawn "amixer -q set Master 10%+")
	, ((shiftMask, 0x1008ff13), spawn "amixer -q set Master 1%+")
	, ((0, 0x1008ff12), spawn "amixer -q set Master toggle")

	-- Keyboard brightness control 
	-- Note that you'll need to make /sys/class/leds/smc::kbd_backlight/brightness writable by xmonad 
	, ((0, 0x1008ff06), spawn "echo 0 > /sys/class/leds/smc::kbd_backlight/brightness")
	, ((0, 0x1008ff05), spawn "echo 255 > /sys/class/leds/smc::kbd_backlight/brightness")

	-- Print Screen
	, ((shiftMask .|. modm, xK_p), spawn "scrot '%Y-%m-%d_$wx$h.png' -e 'mv $f ~shots/'")

	-- Spawn chromium
	, ((modm, xK_c), spawn "chromium")

	-- Spawn gnome-control-center
	, ((modm, xK_g), spawn "gnome-control-center")
	
	-- Terminate application
	, ((modm .|. shiftMask, xK_c     ), kill)

	-- Switch layout
    , ((modm .|. shiftMask, xK_b ), sendMessage NextLayout)
	
	-- Move focus to next
	, ((modm,               xK_Tab   ), windows W.focusDown)
	
	-- Move focus to previous
	, ((modm .|. shiftMask,	xK_Tab   ), windows W.focusUp)
	
	-- Move focus to master
	, ((modm,               xK_m     ), windows W.focusMaster  )

	-- Swap the focused window and the master window
	, ((modm,               xK_Return), windows W.swapMaster)

	-- Shrink the master area
	, ((modm,               xK_h     ), sendMessage Shrink)
	
	-- Expand the master area
	, ((modm,               xK_l     ), sendMessage Expand)
	
	-- Push window back into tiling
	, ((modm,               xK_t     ), withFocused $ windows . W.sink)

	-- toggle the status bar gap (used with avoidStruts from Hooks.ManageDocks)
	, ((modm , xK_b ), sendMessage ToggleStruts)
      
	, ((modm .|. shiftMask, xK_l), spawn "xlock")

	-- Quit xmonad
	, ((modm .|. shiftMask, xK_q     ), io (exitWith ExitSuccess))
	
	-- Restart xmonad
	, ((modm              , xK_q     ), restart "xmonad" True)
	]
	++
	-- mod-[1..9], Switch to workspace N
	-- mod-shift-[1..9], Move client to workspace N
	[((m .|. modm, k), windows $ f i)
		| (i, k) <- zip (XMonad.workspaces conf) [xK_1 .. xK_9]
	    , (f, m) <- [(W.greedyView, 0), (W.shift, shiftMask)]]
	++
	-- mod-{w,e,r}, Switch to physical/Xinerama screens 1, 2, or 3
	-- mod-shift-{w,e,r}, Move client to screen 1, 2, or 3
	[((m .|. modm, key), screenWorkspace sc >>= flip whenJust (windows . f))
		| (key, sc) <- zip [xK_w, xK_e, xK_r] [0..]
		, (f, m) <- [(W.view, 0), (W.shift, shiftMask)]]

myLayoutHook = avoidStruts (smartBorders (tiled ||| Mirror tiled) ||| noBorders Full)
                where
                    tiled   =   Tall nmaster delta ratio
                    nmaster =   1       -- Number of windows in the master panel
                    ratio   =   2%3     -- Percentage of the screen to increment by when resizing the window
                    delta   =   5%100   -- Default portion of the screen occupied by the master panel

myLayout = avoidStruts (
	Tall 1 (3/100) (1/2) |||
	Mirror (Tall 1 (3/100) (1/2)) |||
	noBorders (fullscreenFull Full))

myStartupHook = do
    setWMName "LG3D"

main = do
    xmproc <- spawnPipe "xmobar"
    xmonad $ defaultConfig {
        manageHook = manageDocks <+> manageHook defaultConfig,
        layoutHook = myLayoutHook, 
      	logHook = dynamicLogWithPP xmobarPP {
		      ppOutput = hPutStrLn xmproc,
		      ppTitle = xmobarColor "#f00000" "" . shorten 70
		    },
		terminal = myTerminal,
		modMask = myModMask,
		workspaces = myWorkspaces,
		keys = myKeys,
        borderWidth = myBorderWidth,
		startupHook = myStartupHook,
        normalBorderColor = myNormalBorderColor,
        focusedBorderColor = myFocusedBorderColor,
        focusFollowsMouse = myFocusFollowsMouse
      }
