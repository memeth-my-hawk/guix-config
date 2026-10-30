;; This is an operating system configuration generated
;; by the graphical installer.
;;
;; Once installation is complete, you can learn and modify
;; this file to tweak the system configuration, and pass it
;; to the 'guix system reconfigure' command to effect your
;; changes.


;; Indicate which modules to import to access the variables
;; used in this configuration.
(use-modules (gnu)
	     (gnu services)
	     (guix gexp)
	     (gnu packages window-management)
	     (gnu packages emacs)
	     (gnu packages emacs-xyz)
	     (gnu packages statistics)
	     (gnu packages julia)
	     (gnu packages terminals)
	     (gnu packages pulseaudio)
	     (gnu packages linux)
             (gnu packages cups)
	     (gnu packages gnuzilla)
	     (gnu packages xorg)
	     (gnu packages xdisorg)
	     (gnu packages freedesktop)
	     (gnu packages polkit)
	     (gnu packages admin)
     	     (gnu packages version-control)
	     (gnu packages networking)
	     (gnu packages curl)
	     (gnu packages gnome)
	     (gnu packages lxde)
	     (gnu packages pdf)
	     (gnu packages sync)
	     (gnu packages libreoffice)
	     (gnu packages fonts)
	     (gnu packages rust-apps)		
	     (gnu packages image-viewers)
	     (gnu packages video)

	     (nongnu packages linux)
	     (nongnu packages mozilla)
	     (nongnu packages messaging)
	     (nongnu packages fonts)
	     (nongnu system linux-initrd))

(use-service-modules linux
		     docker
		     admin 
		     sound 
		     dbus 
		     cups 
		     desktop 
		     networking 
		     ssh 
		     pm
		     xorg)

(operating-system
  (kernel linux-lts)
  (initrd microcode-initrd)
  (firmware (list linux-firmware sof-firmware))
  (locale "en_US.utf8")
  (timezone "Europe/Istanbul")
  (keyboard-layout (keyboard-layout "us"))
  (host-name "t14")
  
  (packages (append (list qtile
			  xrandr
			  autorandr
			  xclip
			  polkit-gnome
			  dunst
			  xlockmore
			  xss-lock
		   	  network-manager-applet
			  curl
			  git
			  pulseaudio
			  pavucontrol
			  pulsemixer
			  alsa-utils
			  btop
			  tlp
			  brightnessctl
			  gammastep
			  geoclue
			  fastfetch
			  pcmanfm
			  icecat
			  bluez
			  blueman
			  alacritty
			  zathura
			  zathura-pdf-mupdf
		   	  feh
			  maim
			  scrot
			  mpv
			  ncspot
		  	  libreoffice
			  font-adobe-source-code-pro
			  font-abattis-cantarell
			  font-microsoft-web-core-fonts
			  emacs-no-x
			  emacs-ess
			  emacs-geiser
			  emacs-doom-themes
			  emacs-vertico
			  emacs-orderless
			  emacs-corfu
			  emacs-auctex
 			  emacs-geiser-guile
			  emacs-guix
			  emacs-dirvish
		          rclone
			  udiskie
			  r
			  julia
			  hplip
			  cups-filters
			  firefox-esr		  
			  ) %base-packages))

  ;; The list of user accounts ('root' is implicit).
  (users (cons* 
		(user-account
                  (name "memeth")
                  (comment "memeth")
                  (group "users")
                  (home-directory "/home/memeth")
                  (supplementary-groups '("wheel" "netdev" "audio" "video" "lp" "input")))
                %base-user-accounts))

  ;; Below is the list of system services.  To search for available
  ;; services, run 'guix system search KEYWORD' in a terminal.
  (services
   (append (list
                 (simple-service 'nonguix-substitutes guix-service-type
                     (guix-extension
                        (substitute-urls (list "https://substitutes.nonguix.org"))
                           (authorized-keys (list (plain-file "non-guix.pub"
            "(public-key (ecc (curve Ed25519) (q #C1FD53E5D4CE971933EC50C9F307AE2171A2D3B52C804642A7A35F84F3A4EA98#)))")))))

                 ;; To configure OpenSSH, pass an 'openssh-configuration'
                 ;; record as a second argument to 'service' below.

                 (service openssh-service-type)
		 (service pulseaudio-service-type)
		 (service alsa-service-type)
                 (service network-manager-service-type)
                 (service wpa-supplicant-service-type)
                 (service ntp-service-type)
                 (service gpm-service-type)
		 (service elogind-service-type)
		 (service startx-command-service-type
		 	(xorg-configuration
                   		(extra-config
                    			'("Section \"InputClass\"
    					 	Identifier \"Microsoft Wireless Keyboard TR\"
    						MatchProduct \"Microsoft Bluetooth\"
    						MatchIsKeyboard \"on\"
    						Option \"XkbLayout\" \"tr\"
						EndSection

					  Section \"InputClass\"
    						Identifier \"HP Wired Keyboard Turkish\"
    						MatchIsKeyboard \"on\"
    						MatchProduct \"SIGMACHIP USB Keyboard\"
    						Option \"XkbLayout\" \"tr\"
					  EndSection"))))
		 
		 (service screen-locker-service-type
         		(screen-locker-configuration
           			(name "xlock")
           			(program (file-append xlockmore "/bin/xlock"))))
		 
		 (service tlp-service-type
			(tlp-configuration
				(start-charge-thresh-bat0 85)
          			(stop-charge-thresh-bat0 95)))		 


		 (service dbus-root-service-type)
		 (service polkit-service-type)
		 (service udisks-service-type)
		 (service gvfs-service-type)
		 (service file-database-service-type)
		 (service bluetooth-service-type)
		 (service fstrim-service-type)
	         (service docker-service-type)
		 (service containerd-service-type)
                 (service cups-service-type
         		(cups-configuration
           		  (web-interface? #t)
           		    (extensions
             		      (list cups-filters hplip))))
		 polkit-wheel-service
		 )


           ;; This is the default list of services we
           ;; are appending to.
           %base-services))
  (bootloader (bootloader-configuration
                (bootloader grub-efi-bootloader)
                (targets (list "/boot/efi"))
                (keyboard-layout keyboard-layout)))
  (swap-devices (list (swap-space
                        (target (uuid
                                 "29946673-73b4-4213-ad36-096b653680c0")))))

  ;; The list of file systems that get "mounted".  The unique
  ;; file system identifiers there ("UUIDs") can be obtained
  ;; by running 'blkid' in a terminal.
  (file-systems (cons* (file-system
                         (mount-point "/boot/efi")
                         (device (uuid "6C9B-0E53"
                                       'fat32))
                         (type "vfat"))
                       (file-system
                         (mount-point "/")
                         (device (uuid
                                  "677c5872-dcc9-453f-bb1c-df7560ba2107"
                                  'ext4))
                         (type "ext4")) %base-file-systems)))
