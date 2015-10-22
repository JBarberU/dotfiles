import System.Environment as SysEnv
import System.Exit as SysExit
import System.Process as SysProc
import System.Directory as SysDir
import Data.List as DL

runCmd :: String -> [String] -> IO()
runCmd cmd args = do
  res <- SysProc.system $ DL.intercalate " " ([cmd] ++ args)
  case res of
    ExitSuccess -> return()
    _           -> dropFromRoot >> exitWith res

sudoCmd :: String -> [String] -> IO()
sudoCmd cmd args = runCmd "sudo" ([cmd] ++ args)

dropFromRoot :: IO()
dropFromRoot = do
  _ <- SysProc.system "sudo -k"
  return()

createSymlink :: String -> String -> IO()
createSymlink src dst = runCmd "ln" ["-s", src, dst]

rmRF :: String -> IO()
rmRF path = do
  case path of
    ""  -> putStrLn "Trying to create symlink with empty path" >> exitWith (ExitFailure 1)
    "/" -> putStrLn "Ehh, no?" >> exitWith (ExitFailure 2)
    _   -> runCmd "rm" ["-rf", path]

copyFileDir :: String -> String -> IO()
copyFileDir src dst = runCmd "cp" ["-R", src, dst]

aptInstall :: [String] -> IO()
aptInstall packages = sudoCmd "apt-get" (["install"] ++ packages)

aptUpdate :: IO()
aptUpdate = sudoCmd "apt-get" ["update"]

createDotfileLink :: (String,String) -> IO()
createDotfileLink p = do
  rmRF dst
  createSymlink src dst
    where src = fst p
          dst = snd p

forEach :: (a -> IO()) -> [a] -> IO()
forEach f []          = return()
forEach f (head:tail) = do
  f head
  forEach f tail

installRecipe :: String -> String -> [String] -> [(String, String)]-> IO()
installRecipe cwd home apts dotfiles = do
  aptInstall apts
  forEach createDotfileLink fullDotfiles
    where fullDotfiles = [(cwd ++ "/" ++ src, home ++ "/" ++ dst) | (src, dst) <- dotfiles]

installZsh :: String -> String -> IO()
installZsh cwd home = do
  installRecipe cwd home ["zsh"] dotfiles
    where 
    dotfiles = [
                ("zsh/zshrc", ".zshrc"),
                ("zsh/zsh_env", ".zsh_env"),
                ("zsh/cheat_sheet", ".cheat_sheet"),
                ("zsh/sh_functions", ".sh_functions"),
                ("zsh/oh-my-zsh", ".oh-my-zsh")
               ]

installVim :: String -> String -> IO()
installVim cwd home = do
  installRecipe cwd home apts dotfiles
    where apts = ["vim","exuberant-ctags","ack-grep"]
          dotfiles = [
                      ("vim/vim", ".vim"),
                      ("vim/vimrc", ".vimrc")
                     ]

installXMonad :: String -> String -> IO()
installXMonad cwd home = do
  installRecipe cwd home apts dotfiles
    where apts = ["xmonad", "xmobar", "dmenu", "conky", "scrot", "feh"]
          dotfiles = [
                      ("haskell/ghci", ".ghci"),
                      ("xmonad/xmonad.hs", ".xmonad/xmonad.hs"),
                      ("xmonad/xmobarrc", ".xmobarrc"),
                      ("conky/conkyrc", ".conkyrc"),
                      ("xorg/xinitrc", ".xinitrc")
                     ]

installGit :: String -> String -> IO()
installGit cwd home = do
  installRecipe cwd home apts dotfiles
    where apts = ["git"]
          dotfiles = [
                      ("git/gitignore", ".gitignore"),
                      ("git/gitconfig", ".gitconfig")
                     ]

installRXVT :: String -> String -> IO()
installRXVT cwd home = do
  installRecipe cwd home apts dotfiles
    where apts = ["rxvt-unicode-256color", "xclip"]
          dotfiles = [("xorg/Xresources", ".Xresources")]

installTmux :: String -> String -> IO()
installTmux cwd home = do
  installRecipe cwd home apts dotfiles
    where apts = ["tmux"]
          dotfiles = [
                      ("tmux/tmux.conf", ".tmux.conf"),
                      ("tmux/tmux_powerline.snap", ".tmux_powerline.snap")
                     ]

installIrssi :: String -> String -> IO()
installIrssi cwd home = do
  installRecipe cwd home apts dotfiles
  copyFileDir (home ++ "/.irssi/config.example") (home ++ "/.irssi/config")
    where apts = ["irssi"]
          dotfiles = [("irssi", ".irssi")]

handleArgs :: [String] -> IO()
handleArgs [] = putStrLn "Done!"
handleArgs (arg:args) = do
  cwd <- SysDir.getCurrentDirectory 
  home <- SysDir.getHomeDirectory 
  aptUpdate
  case arg of
    "-h" -> putStrLn "Help"
    "--zsh"    -> installZsh cwd home
    "--vim"    -> installVim cwd home
    "--xmonad" -> installXMonad cwd home
    "--git"    -> installGit cwd home
    "--rxvt"   -> installRXVT cwd home
    "--tmux"   -> installTmux cwd home
    "--irssi"  -> installIrssi cwd home
    "--all"    -> do
                    installZsh cwd home
                    installVim cwd home
                    installXMonad cwd home
                    installGit cwd home
                    installRXVT cwd home
                    installTmux cwd home
                    installIrssi cwd home
    _    -> putStrLn $ "Couldn't parse argument \"" ++ arg ++ "\", try -h"
  handleArgs args
  dropFromRoot
  return()

main :: IO()
main = do
  args <- SysEnv.getArgs
  handleArgs args

