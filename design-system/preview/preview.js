(function () {
  var dropzone = document.getElementById("dropzone");
  var fileInput = document.getElementById("file-input");
  var browseBtn = document.getElementById("browse-btn");
  var fileList = document.getElementById("file-list");

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
        var deleteChip = deleteBtn.closest(".chip");
        if (deleteChip) {
          deleteChip.remove();
        }
        return;
      }

      var chip = event.target.closest(".chip");
      if (chip) {
        chip.classList.toggle("selected");
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
    chip.appendChild(document.createTextNode(email));

    var deleteBtn = document.createElement("span");
    deleteBtn.className = "chip-delete";
    deleteBtn.setAttribute("aria-hidden", "true");
    deleteBtn.textContent = "x";
    chip.appendChild(deleteBtn);

    emailChips.appendChild(chip);
    customEmailInput.value = "";
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

  function cssEscape(value) {
    return value.replace(/(["\\])/g, "\\$1");
  }
})();
