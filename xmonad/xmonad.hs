import XMonad 
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers (isFullscreen, doFullFloat, isDialog, doCenterFloat)
import XMonad.Layout.LayoutModifier (ModifiedLayout)
import XMonad.Layout.Fullscreen()
import XMonad.Layout.NoBorders
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig()
import System.IO
import Data.Ratio ((%))
import XMonad.Hooks.SetWMName
import qualified Data.Map as M
import qualified XMonad.StackSet as W
import System.Exit
import XMonad.Util.NamedScratchpad

myTerminal :: String
myTerminal = "rxvt-unicode"

myNamedTerminal :: String
myNamedTerminal = myTerminal ++ " -name "

myModMask :: KeyMask
myModMask = mod4Mask -- Rebind Mod to the windows key

myBorderWidth :: Dimension
myBorderWidth = 2

myNormalBorderColor :: String
myNormalBorderColor = "black"

myFocusedBorderColor :: String
myFocusedBorderColor = "purple"

myFocusFollowsMouse :: Bool
myFocusFollowsMouse = False

myWorkspaces :: [String]
myWorkspaces = map show ([1..9] :: [Int])

myScratchpads :: [NamedScratchpad]
myScratchpads = 
  let 
    full = customFloating $ W.RationalRect 0.05 0.05 0.9 0.9
    top = customFloating $ W.RationalRect 0.0 0.0 1.0 0.5
    bottom = customFloating $ W.RationalRect 0.0 0.7 1.0 0.3
    browser = "iceweasel"
    --reallyFull = customFloating $ W.RationalRect 0.025 0.025 0.95 0.95
  in
  [NS x y (appName =? z) full | (x,y,z) <-
    [
      ("Browser",       browser, "myBrowser"),
      ("IrssiTerminal", myNamedTerminal ++ "IrssiTerminal -e irssi", "IrssiTerminal"),
      ("AlsaTerminal", myNamedTerminal ++ "AlsaTerminal -e alsamixer", "AlsaTerminal")
    ]
  ]
  ++
  [NS x y (appName =? z) bottom | (x,y,z) <-
    [
      ("BottomTerminal", myNamedTerminal ++ "BottomTerminal", "BottomTerminal")
    ]
  ]
  ++
  [NS x y (appName =? z) top | (x,y,z) <-
    [
      ("TopTerminal", myNamedTerminal ++ "TopTerminal", "TopTerminal")
    ]
  ]

myKeys :: XConfig l -> M.Map (KeyMask, KeySym) (X ())
myKeys conf@(XConfig {XMonad.modMask = modm}) = M.fromList $
  let 
    mshift  = modm .|. shiftMask
    volDown = 0x1008ff11
    volUp   = 0x1008ff13
    mute    = 0x1008ff12
    noMod   = 0
    shift   = shiftMask
  in
  [((modm, x), y) | (x,y) <- 
    [
      (xK_Tab,    windows W.focusDown),
	    (xK_c,      namedScratchpadAction myScratchpads "Calendar"),
	    (xK_m,      namedScratchpadAction myScratchpads "Mail"),
	    (xK_g,      namedScratchpadAction myScratchpads "Browser"),
	    (xK_Return, windows W.swapMaster),
	    (xK_h,      sendMessage Shrink),
	    (xK_s,      sendMessage Expand),
	    (xK_space,  spawn "exe=`cat ~/.dmenu_favourites | dmenu -b ` && eval \"exec $exe\""),
	    (xK_b,      sendMessage ToggleStruts),
      (xK_q,      restart "xmonad" True),
	    (xK_t,      namedScratchpadAction myScratchpads "BottomTerminal"),
      (xK_n,      namedScratchpadAction myScratchpads "TopTerminal"),
      (xK_i,      namedScratchpadAction myScratchpads "IrssiTerminal"),
      (xK_a,      namedScratchpadAction myScratchpads "AlsaTerminal")
    ]
  ]
  ++
  [((mshift, x), y) | (x,y) <- 
    [
      (xK_Return, spawn $ XMonad.terminal conf),
      (xK_space,  spawn "exe=`dmenu_path | dmenu -b ` && eval \"exec $exe\""),
	    (xK_l,      spawn "slock"),
	    (xK_q,      io exitSuccess),
	    (xK_n,      spawn "nautilus"),
	    (xK_t,      withFocused $ windows . W.sink),
	    (xK_Tab,    windows W.focusUp),
	    (xK_p,      spawn "scrot '%Y-%m-%d_$wx$h.png' -e 'mv $f ~shots/'"),
	    (xK_s,      namedScratchpadAction myScratchpads "Spotify"),
	    (xK_g,      spawn "gnome-control-center"),
	    (xK_c,      kill),
      (xK_b,      sendMessage NextLayout)
    ]
  ]
  ++
  [((shift, x), y) | (x,y) <- 
    [
      (volDown,   spawn "amixer -q set Master 1%-"),
	    (volUp,     spawn "amixer -q set Master 1%+")
	  ]
  ]
  ++
  [((noMod, x), y) | (x,y) <- 
    [
      (volDown,   spawn "amixer -q set Master 10%-"),
	    (volUp,     spawn "amixer -q set Master 10%+"),
	    (mute,      spawn "amixer -q set Master toggle")
    ]
  ]
  ++
  -- Workspaces 
	[((m .|. modm, k), windows $ f i)
		| (i, k) <- zip (XMonad.workspaces conf) [xK_1 .. xK_9]
	    , (f, m) <- [(W.greedyView, 0), (W.shift, shiftMask)]]
	++
  -- Screens
	[((m .|. modm, key), screenWorkspace sc >>= flip whenJust (windows . f))
		| (key, sc) <- zip [xK_w, xK_e, xK_r] [0..]
		, (f, m) <- [(W.view, 0), (W.shift, shiftMask)]]

myLayoutHook :: ModifiedLayout AvoidStruts (Choose (ModifiedLayout SmartBorder (Choose Tall (Mirror Tall))) (ModifiedLayout WithBorder Full)) Window
myLayoutHook = avoidStruts $ smartBorders (tiled ||| Mirror tiled) ||| noBorders Full
                where
                    tiled   =   Tall nmaster delta ratio
                    nmaster =   1       -- Number of windows in the master panel
                    ratio   =   2%3     -- Percentage of the screen to increment by when resizing the window
                    delta   =   1%100   -- Default portion of the screen occupied by the master panel

myStartupHook :: X ()
myStartupHook = setWMName "LG3D"

myManageHook :: ManageHook
myManageHook =  composeAll
  [
    (className =? "Xmessage") --> doCenterFloat,
    (className =? "Nvidia-settings") --> doCenterFloat,
    (className =? "Nautilus") --> doCenterFloat,
    isFullscreen --> doFullFloat,
    isDialog --> doCenterFloat
  ]
  <+> manageDocks
  <+> manageHook defaultConfig
  <+> namedScratchpadManageHook myScratchpads

main :: IO ()
main = do
    xmproc <- spawnPipe "xmobar"
    xmonad $ defaultConfig {
        manageHook = myManageHook,
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
