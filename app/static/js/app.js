/**
 * AI Resume Analyser & Job Assistant - Frontend Interactions & Interactivity
 */

document.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
    initFileUploadAndDragDrop();
    initSampleButtons();
    initSampleJDFiller();
    initFormSubmission();
    initAssistantTabs();
    initSTARAccordion();
    initCopyActions();
    initPrintAndDownload();
    initOnePageReportModal();
});

/* ==========================================================================
   Theme Switcher (Dark / Light Mode)
   ========================================================================== */
function initThemeToggle() {
    const toggleBtn = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");
    const htmlElement = document.documentElement;

    // Load saved theme or default to dark
    const savedTheme = localStorage.getItem("resumeai-theme") || "dark";
    htmlElement.setAttribute("data-theme", savedTheme);
    updateThemeIcon(savedTheme);

    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            const currentTheme = htmlElement.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            htmlElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("resumeai-theme", newTheme);
            updateThemeIcon(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeIcon) return;
        if (theme === "light") {
            themeIcon.setAttribute("data-lucide", "sun");
        } else {
            themeIcon.setAttribute("data-lucide", "moon");
        }
        if (window.lucide) {
            lucide.createIcons();
        }
    }
}

/* ==========================================================================
   File Upload & Drag-and-Drop
   ========================================================================== */
function initFileUploadAndDragDrop() {
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("resumeFileInput");
    const promptEl = document.getElementById("dropZonePrompt");
    const previewEl = document.getElementById("filePreview");
    const fileNameDisplay = document.getElementById("fileNameDisplay");
    const fileSizeDisplay = document.getElementById("fileSizeDisplay");
    const btnRemove = document.getElementById("btnRemoveFile");
    const sampleInput = document.getElementById("sampleIdInput");

    if (!dropZone || !fileInput) return;

    // Drag over effects
    ["dragenter", "dragover"].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove("dragover");
        });
    });

    // Handle dropped files
    dropZone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            displaySelectedFile(files[0]);
        }
    });

    // Handle normal file input selection
    fileInput.addEventListener("change", () => {
        if (fileInput.files && fileInput.files.length > 0) {
            displaySelectedFile(fileInput.files[0]);
        }
    });

    // Remove file button
    if (btnRemove) {
        btnRemove.addEventListener("click", (e) => {
            e.stopPropagation();
            fileInput.value = "";
            previewEl.classList.add("hidden");
            promptEl.classList.remove("hidden");
            if (sampleInput) sampleInput.value = "";
        });
    }

    function displaySelectedFile(file) {
        if (promptEl) promptEl.classList.add("hidden");
        if (previewEl) previewEl.classList.remove("hidden");
        if (fileNameDisplay) fileNameDisplay.textContent = file.name;
        if (fileSizeDisplay) fileSizeDisplay.textContent = formatBytes(file.size);
        if (sampleInput) sampleInput.value = ""; // clear sample if real file uploaded
        
        // Clear active class from sample buttons
        document.querySelectorAll(".btn-sample").forEach(b => b.classList.remove("active"));
        showToast(`Selected: ${file.name}`);
    }

    function formatBytes(bytes) {
        if (bytes === 0) return "0 Bytes";
        const k = 1024;
        const sizes = ["Bytes", "KB", "MB", "GB"];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
    }
}

/* ==========================================================================
   Sample Resumes Quick Selectors
   ========================================================================== */
function initSampleButtons() {
    const sampleButtons = document.querySelectorAll(".btn-sample");
    const sampleInput = document.getElementById("sampleIdInput");
    const fileInput = document.getElementById("resumeFileInput");
    const promptEl = document.getElementById("dropZonePrompt");
    const previewEl = document.getElementById("filePreview");
    const fileNameDisplay = document.getElementById("fileNameDisplay");
    const fileSizeDisplay = document.getElementById("fileSizeDisplay");

    sampleButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            sampleButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const sampleId = btn.getAttribute("data-sample");
            if (sampleInput) sampleInput.value = sampleId;
            if (fileInput) fileInput.value = ""; // clear uploaded file

            if (promptEl) promptEl.classList.add("hidden");
            if (previewEl) previewEl.classList.remove("hidden");
            if (fileNameDisplay) fileNameDisplay.textContent = `${sampleId}.txt (Sample Resume)`;
            if (fileSizeDisplay) fileSizeDisplay.textContent = "Preset Profile Ready";

            showToast(`Loaded sample resume: ${btn.textContent.trim()}`);
        });
    });
}

/* ==========================================================================
   Sample Job Description Filler
   ========================================================================== */
function initSampleJDFiller() {
    const btnPasteJD = document.getElementById("btnPasteSampleJD");
    const jdTextarea = document.getElementById("jobDescriptionInput");

    const SAMPLE_JOB_DESCRIPTION = `Senior Full-Stack Engineer / Cloud Systems Lead

About the Role:
We are looking for a Senior Software Engineer with strong expertise in Python, FastAPI or Django, React/Next.js, PostgreSQL, Docker, and AWS cloud architecture. You will lead the design and deployment of distributed high-throughput microservices, optimize system latency, and collaborate across engineering teams in an Agile environment.

Requirements & Qualifications:
• 5+ years of experience with Python, FastAPI/Django, and modern JavaScript/TypeScript (React).
• Proven track record with relational databases (PostgreSQL), Redis caching, and database query tuning.
• Strong hands-on experience with Docker, Kubernetes, CI/CD pipelines (GitHub Actions), and AWS (ECS, Lambda, S3, RDS).
• Deep understanding of microservices, RESTful API design, GraphQL, and System Design.
• Experience mentoring engineers, conducting code reviews, and working in cross-functional Agile/Scrum teams.
• Bonus: Experience with AI/LLM integration (LangChain), Terraform, or Prometheus monitoring.`;

    if (btnPasteJD && jdTextarea) {
        btnPasteJD.addEventListener("click", () => {
            jdTextarea.value = SAMPLE_JOB_DESCRIPTION;
            jdTextarea.focus();
            showToast("Sample Job Description loaded!");
        });
    }
}

/* ==========================================================================
   Form Submit Loading Animation
   ========================================================================== */
function initFormSubmission() {
    const form = document.getElementById("resumeForm");
    const btnSubmit = document.getElementById("btnSubmit");
    const spinner = document.getElementById("submitSpinner");
    const btnText = btnSubmit ? btnSubmit.querySelector(".btn-text") : null;
    const fileInput = document.getElementById("resumeFileInput");
    const sampleInput = document.getElementById("sampleIdInput");

    if (form && btnSubmit) {
        form.addEventListener("submit", (e) => {
            const hasFile = fileInput && fileInput.files && fileInput.files.length > 0;
            const hasSample = sampleInput && sampleInput.value.trim() !== "";

            if (!hasFile && !hasSample) {
                e.preventDefault();
                showToast("Please upload a resume file or select a sample preset first!");
                return;
            }

            // Show spinner
            if (spinner) spinner.classList.remove("hidden");
            if (btnText) btnText.innerHTML = `<i data-lucide="loader"></i> Parsing & Analyzing ATS Metrics...`;
            btnSubmit.style.pointerEvents = "none";
            btnSubmit.style.opacity = "0.85";
            if (window.lucide) lucide.createIcons();
        });
    }
}

/* ==========================================================================
   AI Job Assistant Tabs Navigation
   ========================================================================== */
function initAssistantTabs() {
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTabId = btn.getAttribute("data-tab");

            tabButtons.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            const targetEl = document.getElementById(targetTabId);
            if (targetEl) {
                targetEl.classList.add("active");
            }
        });
    });
}

/* ==========================================================================
   STAR Interview Accordion
   ========================================================================== */
function initSTARAccordion() {
    const accordionItems = document.querySelectorAll(".accordion-item");

    accordionItems.forEach((item, index) => {
        // Open the first question by default
        if (index === 0) item.classList.add("open");

        const header = item.querySelector(".accordion-header");
        if (header) {
            header.addEventListener("click", () => {
                item.classList.toggle("open");
            });
        }
    });
}

/* ==========================================================================
   Copy to Clipboard Actions
   ========================================================================== */
function initCopyActions() {
    // Copy Cover Letter
    const btnCopyCoverLetter = document.getElementById("btnCopyCoverLetter");
    const coverLetterText = document.getElementById("coverLetterText");
    if (btnCopyCoverLetter && coverLetterText) {
        btnCopyCoverLetter.addEventListener("click", () => {
            copyTextToClipboard(coverLetterText.value, "Cover letter copied to clipboard!");
        });
    }

    // Copy Targeted Textareas (Outreach notes)
    document.querySelectorAll(".btn-icon-copy").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-copy-target");
            const targetEl = document.getElementById(targetId);
            if (targetEl) {
                copyTextToClipboard(targetEl.value, "Copied to clipboard!");
            }
        });
    });

    // Copy Enhanced Bullets
    document.querySelectorAll(".btn-copy-sm").forEach(btn => {
        btn.addEventListener("click", () => {
            const textToCopy = btn.getAttribute("data-copy-text");
            if (textToCopy) {
                copyTextToClipboard(textToCopy, "Enhanced bullet point copied!");
            }
        });
    });
}

function copyTextToClipboard(text, successMsg) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(successMsg || "Copied to clipboard!");
        }).catch(() => {
            fallbackCopy(text, successMsg);
        });
    } else {
        fallbackCopy(text, successMsg);
    }
}

function fallbackCopy(text, successMsg) {
    const tempInput = document.createElement("textarea");
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);
    showToast(successMsg || "Copied to clipboard!");
}

/* ==========================================================================
   Print & Download Actions
   ========================================================================== */
function initPrintAndDownload() {
    const btnPrint = document.getElementById("btnPrintReport");
    if (btnPrint) {
        btnPrint.addEventListener("click", () => {
            window.print();
        });
    }

    const btnDownloadLetter = document.getElementById("btnDownloadCoverLetter");
    const coverLetterText = document.getElementById("coverLetterText");
    if (btnDownloadLetter && coverLetterText) {
        btnDownloadLetter.addEventListener("click", () => {
            const blob = new Blob([coverLetterText.value], { type: "text/plain;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "Tailored_Cover_Letter.txt";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast("Cover letter downloaded!");
        });
    }
}

/* ==========================================================================
   1-Page Executive Report Modal & Print Controller
   ========================================================================== */
function initOnePageReportModal() {
    const modal = document.getElementById("onePageReportModal");
    const btnOpen = document.getElementById("btnOpenOnePageReport");
    const btnClose = document.getElementById("btnCloseOnePageModal");
    const btnPrintSheet = document.getElementById("btnPrintOnePageSheet");
    const btnCopySummary = document.getElementById("btnCopyOnePageSummary");

    if (!modal) return;

    function openModal() {
        modal.classList.remove("hidden");
        document.body.style.overflow = "hidden";
        if (window.lucide) lucide.createIcons();
    }

    function closeModal() {
        modal.classList.add("hidden");
        document.body.style.overflow = "";
    }

    if (btnOpen) {
        btnOpen.addEventListener("click", openModal);
    }

    if (btnClose) {
        btnClose.addEventListener("click", closeModal);
    }

    // Close on backdrop click
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Close on Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !modal.classList.contains("hidden")) {
            closeModal();
        }
    });

    // Print 1-Page Sheet strictly on 1 physical/PDF page
    if (btnPrintSheet) {
        btnPrintSheet.addEventListener("click", () => {
            document.body.classList.add("print-one-page-only");
            window.print();
            
            // Clean up class after printing dialog closes
            window.addEventListener("afterprint", () => {
                document.body.classList.remove("print-one-page-only");
            }, { once: true });
            
            // Fallback timeout in case afterprint doesn't fire
            setTimeout(() => {
                document.body.classList.remove("print-one-page-only");
            }, 1000);
        });
    }

    // Copy formatted executive text summary
    if (btnCopySummary) {
        btnCopySummary.addEventListener("click", () => {
            const sheet = document.getElementById("onePageSheet");
            if (!sheet) return;

            const name = sheet.querySelector(".opr-name")?.textContent.trim() || "Candidate";
            const role = sheet.querySelector(".opr-target-role")?.textContent.trim() || "Role";
            const score = sheet.querySelector(".opr-score-num")?.textContent.trim() || "N/A";
            const badge = sheet.querySelector(".opr-badge-pill")?.textContent.trim() || "";
            const verdict = sheet.querySelector(".opr-verdict-text")?.textContent.trim() || "";

            const summaryText = `======================================================
AI RESUME ANALYSER — 1-PAGE EXECUTIVE ATS REPORT
======================================================
Candidate: ${name} (${role})
Overall ATS Score: ${score}/100 [${badge}]

EXECUTIVE ATS VERDICT:
${verdict}

Generated by ResumeAI PRO Engine.
======================================================`;

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(summaryText).then(() => {
                    showToast("Executive summary copied!");
                });
            } else {
                const tempInput = document.createElement("textarea");
                tempInput.value = summaryText;
                document.body.appendChild(tempInput);
                tempInput.select();
                document.execCommand("copy");
                document.body.removeChild(tempInput);
                showToast("Executive summary copied!");
            }
        });
    }
}

/* ==========================================================================
   Toast Notification System
   ========================================================================== */
function showToast(message) {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = "toast-message";
    toast.innerHTML = `<i data-lucide="check-circle" style="width:16px;height:16px;"></i> <span>${message}</span>`;
    container.appendChild(toast);

    if (window.lucide) lucide.createIcons();

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(10px)";
        toast.style.transition = "all 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}
