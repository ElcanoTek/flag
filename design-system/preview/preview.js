(function () {
  var dropzone = document.getElementById("dropzone");
  var fileInput = document.getElementById("file-input");
  var browseBtn = document.getElementById("browse-btn");
  var fileList = document.getElementById("file-list");
  var announcer = document.getElementById("previewAnnouncer");
  var processingStatus = document.getElementById("processingStatus");
  var THEME_STORAGE_KEY = "flag-theme-preference";
  var THEME_LIGHT = "light";
  var THEME_DARK = "dark";
  var THEME_SYSTEM = "system";

  if (dropzone && fileInput && browseBtn) {
    var setDrag = function (enabled) {
      dropzone.classList.toggle("is-dragover", enabled);
    };

    ["dragenter", "dragover"].forEach(function (eventName) {
      dropzone.addEventListener(eventName, function (event) {
        event.preventDefault();
        setDrag(true);
      });
    });

    ["dragleave", "drop"].forEach(function (eventName) {
      dropzone.addEventListener(eventName, function (event) {
        event.preventDefault();
        setDrag(false);
      });
    });

    dropzone.addEventListener("drop", function (event) {
      if (!event.dataTransfer || !event.dataTransfer.files.length) {
        return;
      }
      renderFiles(event.dataTransfer.files);
    });

    browseBtn.addEventListener("click", function () {
      fileInput.click();
    });

    fileInput.addEventListener("change", function () {
      if (!fileInput.files || !fileInput.files.length) {
        return;
      }
      renderFiles(fileInput.files);
    });
  }

  function renderFiles(files) {
    if (!fileList) {
      return;
    }

    var html = [];
    for (var i = 0; i < files.length; i += 1) {
      var file = files[i];
      var sizeMb = (file.size / (1024 * 1024)).toFixed(2);
      html.push(
        '<div class="file-item">' +
          '<span class="file-item-icon">#</span>' +
          '<div class="file-item-info">' +
            '<span class="file-item-name">' + escapeHtml(file.name) + '</span>' +
            '<span class="file-item-size">' + sizeMb + ' MB</span>' +
          '</div>' +
          '<div class="file-item-actions"><span class="file-item-percent">queued</span></div>' +
        '</div>'
      );
    }
    fileList.innerHTML = html.join("");
    if (processingStatus) {
      processingStatus.innerHTML = '<span class="spinner" aria-hidden="true"></span> ' + files.length + ' file' + (files.length === 1 ? '' : 's') + ' queued for processing.';
    }
    announce(files.length + ' file' + (files.length === 1 ? '' : 's') + ' added.');
  }

  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  var numberInputs = document.querySelectorAll("[data-number-input]");
  numberInputs.forEach(function (container) {
    var field = container.querySelector(".number-input__field");
    if (!field) {
      return;
    }

    container.querySelectorAll(".number-input__btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var step = Number(btn.getAttribute("data-step")) || 0;
        var current = Number(field.value || 0);
        var min = field.min === "" ? Number.NEGATIVE_INFINITY : Number(field.min);
        var max = field.max === "" ? Number.POSITIVE_INFINITY : Number(field.max);
        var next = current + step;
        next = Math.min(max, Math.max(min, next));
        field.value = String(next);
        field.dispatchEvent(new Event("input", { bubbles: true }));
      });
    });
  });

  var expandAllBtn = document.getElementById("expandAllSections");
  var collapseAllBtn = document.getElementById("collapseAllSections");
  var toggleThemeBtn = document.getElementById("toggleTheme");
  var toggleThemeBtnText = toggleThemeBtn ? toggleThemeBtn.querySelector("[data-theme-toggle-text]") : null;
  var sectionAccordions = document.querySelectorAll(".section-accordion");
  var themeLogos = document.querySelectorAll(".theme-logo[data-logo-dark][data-logo-light]");
  var rootElement = document.documentElement;
  var systemThemeMedia = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  var activeThemePreference = THEME_SYSTEM;

  if (expandAllBtn) {
    expandAllBtn.addEventListener("click", function () {
      sectionAccordions.forEach(function (accordion) {
        accordion.open = true;
      });
    });
  }

  if (collapseAllBtn) {
    collapseAllBtn.addEventListener("click", function () {
      sectionAccordions.forEach(function (accordion) {
        accordion.open = false;
      });
    });
  }

  function getStoredThemePreference() {
    try {
      var stored = window.localStorage.getItem(THEME_STORAGE_KEY);
      if (stored === THEME_LIGHT || stored === THEME_DARK || stored === THEME_SYSTEM) {
        return stored;
      }
    } catch (error) {
      return THEME_SYSTEM;
    }

    return THEME_SYSTEM;
  }

  function saveThemePreference(preference) {
    try {
      if (preference === THEME_SYSTEM) {
        window.localStorage.removeItem(THEME_STORAGE_KEY);
        return;
      }
      window.localStorage.setItem(THEME_STORAGE_KEY, preference);
    } catch (error) {
      // Ignore storage failures and keep theme in memory.
    }
  }

  function getSystemTheme() {
    if (systemThemeMedia && systemThemeMedia.matches) {
      return THEME_DARK;
    }
    return THEME_LIGHT;
  }

  function resolveTheme(preference) {
    if (preference === THEME_LIGHT || preference === THEME_DARK) {
      return preference;
    }
    return getSystemTheme();
  }

  function updateThemeToggleUi(activeTheme) {
    if (!toggleThemeBtn) {
      return;
    }

    var isDarkTheme = activeTheme === THEME_DARK;
    toggleThemeBtn.setAttribute("aria-pressed", isDarkTheme ? "true" : "false");
    toggleThemeBtn.setAttribute("aria-label", isDarkTheme ? "Switch to light mode" : "Switch to dark mode");
    toggleThemeBtn.setAttribute("title", isDarkTheme ? "Dark mode" : "Light mode");

    if (toggleThemeBtnText) {
      toggleThemeBtnText.textContent = isDarkTheme ? "Dark mode" : "Light mode";
    }
  }

  function updateThemeLogos(activeTheme) {
    var useLightAsset = activeTheme === THEME_LIGHT;

    themeLogos.forEach(function (img) {
      var nextSrc = useLightAsset ? img.getAttribute("data-logo-light") : img.getAttribute("data-logo-dark");
      if (nextSrc && img.getAttribute("src") !== nextSrc) {
        img.setAttribute("src", nextSrc);
      }
    });
  }

  function applyTheme(activeTheme, announceChange) {
    rootElement.setAttribute("data-theme", activeTheme);
    document.body.classList.toggle("theme-light", activeTheme === THEME_LIGHT);
    updateThemeToggleUi(activeTheme);
    updateThemeLogos(activeTheme);

    if (announceChange) {
      announce("Theme set to " + activeTheme + " mode.");
    }
  }

  function setThemePreference(nextPreference, announceChange) {
    activeThemePreference = nextPreference;
    saveThemePreference(nextPreference);
    applyTheme(resolveTheme(nextPreference), announceChange);
  }

  setThemePreference(getStoredThemePreference(), false);

  if (toggleThemeBtn) {
    toggleThemeBtn.addEventListener("click", function () {
      var currentTheme = rootElement.getAttribute("data-theme") === THEME_DARK ? THEME_DARK : THEME_LIGHT;
      var nextTheme = currentTheme === THEME_DARK ? THEME_LIGHT : THEME_DARK;
      setThemePreference(nextTheme, true);
    });
  }

  function syncThemeWithSystem(event) {
    if (activeThemePreference !== THEME_SYSTEM) {
      return;
    }

    var systemTheme = event && event.matches ? THEME_DARK : getSystemTheme();
    applyTheme(systemTheme, true);
  }

  if (systemThemeMedia) {
    if (typeof systemThemeMedia.addEventListener === "function") {
      systemThemeMedia.addEventListener("change", syncThemeWithSystem);
    } else if (typeof systemThemeMedia.addListener === "function") {
      systemThemeMedia.addListener(syncThemeWithSystem);
    }
  }

  if (typeof window.flatpickr === "function") {
    document.querySelectorAll(".custom-datepicker").forEach(function (input) {
      var isDateTime = input.classList.contains("custom-datetimepicker");

      if (input._flatpickr) {
        input._flatpickr.destroy();
      }

      window.flatpickr(input, {
        allowInput: true,
        enableTime: isDateTime,
        noCalendar: false,
        time_24hr: true,
        dateFormat: isDateTime ? "Y-m-d H:i" : "Y-m-d",
        defaultDate: isDateTime ? "today" : null,
        clickOpens: true
      });
    });
  }

  var emailChips = document.getElementById("emailChipsPreview");
  var customEmailInput = document.getElementById("customEmailPreviewInput");
  var addEmailBtn = document.getElementById("addEmailPreviewBtn");

  if (emailChips) {
    emailChips.addEventListener("click", function (event) {
      var deleteBtn = event.target.closest(".chip-delete");
      if (deleteBtn) {
        event.stopPropagation();
        var deleteChip = deleteBtn.closest(".chip");
        if (deleteChip) {
          announce('Removed recipient ' + (deleteChip.dataset.email || ''));
          deleteChip.remove();
        }
        return;
      }

      var chip = event.target.closest(".chip");
      if (chip) {
        var selected = chip.classList.toggle("selected");
        var toggle = chip.querySelector(".chip-toggle");
        if (toggle) {
          toggle.setAttribute("aria-pressed", selected ? "true" : "false");
        }
        announce((selected ? 'Selected ' : 'Deselected ') + (chip.dataset.email || 'recipient'));
      }
    });
  }

  function addCustomEmailPill() {
    if (!emailChips || !customEmailInput) {
      return;
    }

    var email = String(customEmailInput.value || "").trim().toLowerCase();
    if (!email) {
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      customEmailInput.focus();
      return;
    }

    if (emailChips.querySelector('.chip[data-email="' + cssEscape(email) + '"]')) {
      customEmailInput.value = "";
      return;
    }

    var chip = document.createElement("span");
    chip.className = "chip chip-email selected";
    chip.dataset.email = email;

    var toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className = "chip-toggle";
    toggleBtn.setAttribute("aria-pressed", "true");
    toggleBtn.textContent = email;
    chip.appendChild(toggleBtn);

    var deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "chip-delete";
    deleteBtn.setAttribute("aria-label", "Remove recipient " + email);
    deleteBtn.textContent = "x";
    chip.appendChild(deleteBtn);

    emailChips.appendChild(chip);
    customEmailInput.value = "";
    announce('Added recipient ' + email);
  }

  if (addEmailBtn) {
    addEmailBtn.addEventListener("click", addCustomEmailPill);
  }

  if (customEmailInput) {
    customEmailInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        addCustomEmailPill();
      }
    });
  }

  // Color swatches show the live token value for the current theme.
  function refreshSwatches() {
    var styles = window.getComputedStyle(document.documentElement);
    Array.prototype.forEach.call(document.querySelectorAll(".swatch[data-token]"), function (swatch) {
      var label = swatch.querySelector("[data-token-value]");
      var value = styles.getPropertyValue(swatch.getAttribute("data-token")).trim();
      if (label && value) {
        label.textContent = value.toUpperCase();
      }
    });
  }
  refreshSwatches();
  new MutationObserver(refreshSwatches).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

  // The demo header's theme toggle drives the page toggle.
  Array.prototype.forEach.call(document.querySelectorAll("[data-preview-theme-proxy]"), function (proxy) {
    proxy.addEventListener("click", function () {
      var main = document.getElementById("toggleTheme");
      if (main) {
        main.click();
      }
    });
  });

  // Segmented controls: a button group with one aria-pressed option.
  Array.prototype.forEach.call(document.querySelectorAll('.seg[role="group"]'), function (group) {
    group.addEventListener("click", function (event) {
      var option = event.target.closest(".seg-option");
      if (!option || option.disabled) {
        return;
      }
      Array.prototype.forEach.call(group.querySelectorAll(".seg-option"), function (other) {
        other.setAttribute("aria-pressed", other === option ? "true" : "false");
      });
    });
  });

  function cssEscape(value) {
    return value.replace(/(["\\])/g, "\\$1");
  }

  function announce(message) {
    if (!announcer) {
      return;
    }
    announcer.textContent = "";
    window.setTimeout(function () {
      announcer.textContent = message;
    }, 10);
  }
})();
