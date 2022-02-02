import XMonad
import XMonad.Config.Desktop (desktopConfig)
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers (isFullscreen, doFullFloat, isDialog, doCenterFloat)
import XMonad.Layout.LayoutModifier (ModifiedLayout)
import XMonad.Layout.Fullscreen()
import XMonad.Layout.Spacing
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

data ScrotMode    = Normal | RectSelect
data VolumeMode   = Up | Down | Mute
data RhythmAction = RANext | RAPrev | RAPlayPause

myTerminal :: String
myTerminal = "rxvt-unicode"

myNamedTerminal :: String
myNamedTerminal = myTerminal ++ " -name "

myModMask :: KeyMask
myModMask = mod4Mask -- Rebind Mod to the windows key

myBorderWidth :: Dimension
myBorderWidth = 2

myNormalBorderColor :: String
myNormalBorderColor = "#1d2021"

myFocusedBorderColor :: String
myFocusedBorderColor = "#b16286"

myFocusFollowsMouse :: Bool
{-myFocusFollowsMouse = True-}
myFocusFollowsMouse = False

myWorkspaces :: [String]
myWorkspaces = map show [1..9]

scrot :: ScrotMode -> X()
scrot m = spawn fullCmd
  where fullCmd   = preCmd ++ scrotCmd ++ "'%Y-%m-%d-%H_%M_%S_$wx$h.png' -e 'mv $f ~/shots/'"
        scrotCmd  = "scrot " ++ case m of
                                  RectSelect -> "-s "
                                  otherwise  -> ""
        preCmd    = case m of
                      RectSelect -> "sleep 0.2; "
                      otherwise  -> ""

volume :: VolumeMode -> Int -> X()
volume Mute _ = spawn "amixer -q set Master toggle"
volume d x   = spawn cmd
  where cmd = "amixer -q set Master " ++ (show x) ++ "%" ++ case d of
                                                              Up -> "+"
                                                              Down -> "-"

rhythmbox :: RhythmAction -> X()
rhythmbox a = spawn ("rhythmbox-client " ++ action)
  where action = case a of 
                  RANext      -> "--next"
                  RAPrev      -> "--prev"
                  RAPlayPause -> "--play-pause"

myScratchpads :: [NamedScratchpad]
myScratchpads =
  let
    full = customFloating $ W.RationalRect 0.05 0.05 0.9 0.9
    top = customFloating $ W.RationalRect 0.0 0.0 1.0 0.5
    bottom = customFloating $ W.RationalRect 0.0 0.7 1.0 0.3
    browser = "firefox"
    --reallyFull = customFloating $ W.RationalRect 0.025 0.025 0.95 0.95
  in
  [NS x y (appName =? z) full | (x,y,z) <-
    [
      ("Browser",       browser, "myBrowser"),
      ("IrssiTerminal", myNamedTerminal ++ "IrssiTerminal -e irssi", "IrssiTerminal"),
      ("AlsaTerminal", myNamedTerminal ++ "AlsaTerminal -e alsamixer", "AlsaTerminal"),
      ("FullTerminal", myNamedTerminal ++ "FullTerminal", "FullTerminal")
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
    volDownBtn  = 0x1008ff11
    volUpBtn    = 0x1008ff13
    muteBtn     = 0x1008ff12
    noMod       = 0
    shift       = shiftMask
  in
  [((modm, x), y) | (x,y) <-
    [
      (xK_Tab,    windows W.focusDown),
      (xK_c,      spawn "gnome-calculator"),
      (xK_m,      namedScratchpadAction myScratchpads "Mail"),
      (xK_g,      namedScratchpadAction myScratchpads "Browser"),
      (xK_Return, windows W.swapMaster),
      (xK_space,  spawn "rofi -show run"),
      (xK_h,      sendMessage Shrink),
      (xK_l,      sendMessage Expand),
      (xK_p,      scrot Normal),
      (xK_b,      sendMessage ToggleStruts),
      (xK_q,      spawn "xmonad --recompile; xmonad --restart"),
      (xK_t,      namedScratchpadAction myScratchpads "BottomTerminal"),
      (xK_n,      namedScratchpadAction myScratchpads "TopTerminal"),
      (xK_i,      namedScratchpadAction myScratchpads "IrssiTerminal"),
      (xK_s,      namedScratchpadAction myScratchpads "FullTerminal"),
      (xK_a,      namedScratchpadAction myScratchpads "AlsaTerminal")
    ]
  ]
  ++
  [((mshift, x), y) | (x,y) <-
    [
      (xK_Return,   spawn $ XMonad.terminal conf),
      (xK_l,        spawn "slock"),
      (xK_q,        io (exitWith ExitSuccess)),
      (xK_n,        spawn "nautilus"),
      (xK_t,        withFocused $ windows . W.sink),
      (xK_Tab,      windows W.focusUp),
      (xK_p,        scrot RectSelect),
      (xK_s,        namedScratchpadAction myScratchpads "Spotify"),
      (xK_g,        spawn "gnome-control-center"),
      (xK_c,        kill),
      (xK_b,        sendMessage NextLayout),
      (volDownBtn,  rhythmbox RAPrev),
      (volUpBtn,    rhythmbox RANext),
      (muteBtn,     rhythmbox RAPlayPause)
    ]
  ]
  ++
  [((shift, x), y) | (x,y) <-
    [
      (volDownBtn, volume Down 1),
      (volUpBtn,   volume Up   1)
    ]
  ]
  ++
  [((noMod, x), y) | (x,y) <-
    [
      (volDownBtn,   volume Down 10),
      (volUpBtn,     volume Up   10),
      (muteBtn,      volume Mute 0)
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

myLayoutHook :: ModifiedLayout AvoidStruts (Choose (ModifiedLayout Spacing Tall) (Choose (Mirror (ModifiedLayout Spacing Tall)) (ModifiedLayout WithBorder Full))) Window
myLayoutHook = avoidStruts $ tiled ||| Mirror tiled ||| noBorders Full
                where
                    tiled   =   smartSpacing 8 (Tall nmaster delta ratio)
                    nmaster =   1       -- Number of windows in the master panel
                    ratio   =   2%3     -- Percentage of the screen to increment by when resizing the window
                    delta   =   1%100   -- Default portion of the screen occupied by the master panel

myStartupHook :: X ()
myStartupHook = setWMName "LG3D"

myManageHook :: ManageHook
myManageHook =  composeAll
  [
    (className =? "zoom") --> doCenterFloat,
    (className =? "Gnome-calculator") --> doCenterFloat,
    (className =? "Xmessage") --> doCenterFloat,
    (className =? "Nvidia-settings") --> doCenterFloat,
    (className =? "Steam") --> doFloat,
    (className =? "Friends") --> doCenterFloat,
    (className =? "Nautilus") --> doCenterFloat,
    (className =? "Dreamler") --> doCenterFloat,
    (className =? "DreamlerDebug") --> doCenterFloat,
    isFullscreen --> doFullFloat,
    isDialog --> doCenterFloat
  ]
  <+> manageDocks
  <+> manageHook defaultConfig
  <+> namedScratchpadManageHook myScratchpads

main :: IO ()
main = do
    xmproc <- spawnPipe "xmobar"
    xmonad $ desktopConfig {
        manageHook = myManageHook,
        layoutHook = myLayoutHook,
        logHook = dynamicLogWithPP xmobarPP {
          ppOutput = hPutStrLn xmproc,
          ppTitle = xmobarColor "#d3869b" "" . shorten 70
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
