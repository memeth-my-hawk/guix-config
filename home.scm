(use-modules (gnu home)
             (gnu home services)
             (gnu home services shells)
             (gnu home services shepherd)
             (gnu home services xdg)
             (gnu services)
             (guix gexp))

(home-environment
 ;; Packages block removed. You can continue managing packages 
 ;; via `guix install` or a separate `manifest.scm`.
 
 (services
  (list
   
   ;; 1. XINITRC GENERATION
   (simple-service 'qtile-xinitrc
                   home-files-service-type
                   `((".xinitrc" ,(local-file "dotfiles/xinitrc"))))

   ;; 2. XDG CONFIGURATION FILES
   ;; Uses local-file to pull from the "files/" directory next to this home.scm
   (simple-service 'my-xdg-configs
                   home-xdg-configuration-files-service-type
                   `(("qtile/config.py" ,(local-file "dotfiles/qtile/config.py"))
		     ;;("qtile/autostart.sh" ,(local-file "dotfiles/qtile/autostart.sh"))
                     ("alacritty/alacritty.toml" ,(local-file "dotfiles/alacritty/alacritty.toml"))
                     ("emacs/init.el" ,(local-file "dotfiles/emacs/init.el"))
		     ("btop/btop.conf", (local-file "dotfiles/btop/btop.conf"))
		     ("guix/channels.scm" ,(local-file "dotfiles/guix/channels.scm"))))

   ;; 3. SHEPHERD BACKGROUND DAEMONS
   (service home-shepherd-service-type
            (home-shepherd-configuration
             (services
              (list
               (shepherd-service
                (provision '(emacs-daemon))
                (start #~(make-forkexec-constructor '("emacs" "--daemon")))
                (stop #~(make-kill-destructor)))))))

   ;; 4. BASH ENVIRONMENT & ALIASES
   (service home-bash-service-type
            (home-bash-configuration
             (environment-variables
              '(("EDITOR" . "emacsclient -c -a emacs")
                ("VISUAL" . "emacsclient -c -a emacs")))
             (aliases
              '(("ll" . "ls -la --color=auto")
                ("r"  . "R --quiet")
                ("sys-update" . "sudo guix system reconfigure ~/guix-config/config.scm")
                ("home-update" . "guix home reconfigure ~/guix-config/home.scm")))))

   )))
