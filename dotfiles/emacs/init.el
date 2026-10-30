;;; 1. BARE-METAL UI SETTINGS
;; Strip the 1990s GUI clutter instantly
(setq inhibit-startup-message t)
(scroll-bar-mode -1)
(tool-bar-mode -1)
(tooltip-mode -1)
(menu-bar-mode -1)

;; Sane typing defaults
(setq-default indent-tabs-mode nil) ; Use spaces, never tabs
(column-number-mode)
(global-display-line-numbers-mode t)
;; Disable line numbers in specific reading modes like Org
(dolist (mode '(org-mode-hook term-mode-hook shell-mode-hook eshell-mode-hook))
  (add-hook mode (lambda () (display-line-numbers-mode 0))))

;;; 2. THEME
(use-package doom-themes
  :ensure t
  :config
  (setq doom-themes-enable-bold t
        doom-themes-enable-italic t)
  (load-theme 'doom-solarized-light t)
  (doom-themes-org-config))

;;; 3. CORE MODERN MINIBUFFER (Vertico + Orderless)
(use-package vertico
  :ensure t
  :init (vertico-mode))

(use-package orderless
  :ensure t
  :custom
  (completion-styles '(orderless basic))
  (completion-category-overrides '((file (styles basic partial-completion)))))

;;; 4. IN-BUFFER AUTO-COMPLETION (Corfu)
(use-package corfu
  :ensure t
  :custom
  (corfu-auto t)          ; Enable auto completion
  (corfu-quit-no-match t) ; Quit if there is no match
  :init
  (global-corfu-mode))

;;; 5. R & STATISTICS (ESS)
(use-package ess
  :ensure t
  :init
  (require 'ess-site)
  :custom
  (ess-ask-for-ess-directory nil) ; Don't annoy with dir prompts
  (ess-style 'RRR))               ; Standard R indentation style

;;; 6. LATEX (AUCTeX)
(use-package tex
  :ensure auctex
  :custom
  (TeX-auto-save t)
  (TeX-parse-self t)
  (TeX-master nil)
  ;; Automatically compile to PDF
  (TeX-PDF-mode t))

;;; 7. GUIX SCHEME (Geiser)
(use-package geiser
  :ensure t
  :custom
  (geiser-active-implementations '(guile)))

(use-package geiser-guile
  :ensure t)

;;; 8. ORG MODE (Notes & Journaling)
(use-package org
  ;; Built-in, no :ensure needed
  :custom
  (org-hide-emphasis-markers t)   ; Hide *bold* and /italic/ markers
  (org-src-fontify-natively t)    ; Colorize code blocks identically to their native modes
  (org-src-tab-acts-natively t)
  (org-edit-src-content-indentation 0)
  (org-log-done 'time)            ; Timestamp when a TODO is marked done
  ;; Define where your notes live
  (org-directory "~/Documents/Org")
  (org-default-notes-file (concat org-directory "/journal.org")))
