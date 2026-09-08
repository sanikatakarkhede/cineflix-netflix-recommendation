/**
 * CineFlix - Frontend Application Logic
 * Authentication-First Architecture, Dual-Theme (Light / Dark),
 * User Authentication & Guest Sessions, Protected Feature Interceptions,
 * Dynamic NLP Preference Vector Recommender & CineBot AI Curator.
 */

// Centralized Application State
const state = {
    authState: "unauthenticated", // "unauthenticated" | "guest" | "authenticated"
    isAuthenticated: false,
    isGuest: false,
    currentUser: null,
    activePersona: "sci_fi_geek",
    userProfile: null,
    recommendations: [],
    becauseWatched: null,
    allMovies: [],
    genres: [],
    moods: [],
    activeMood: "all",
    activeType: "All",
    activeGenre: "All",
    activeLanguage: "All",
    activeIndustry: "All",
    activeCountry: "All",
    activeSort: "default",
    searchQuery: "",
    chatContext: {},
    chatMessages: [],
    selectedMovieId: null,
    theme: "dark",
    isColdStart: false,
    
    // Hero Slider State
    heroSlides: [],
    activeHeroIndex: 0,
    heroTimer: null,
    isVoiceRecording: false
};

// Speech Recognition instance
let recognition = null;
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";
}

// DOM Elements
const elements = {
    // Views and Containers
    authHeader: document.getElementById("auth-header"),
    authWelcomeScreen: document.getElementById("auth-welcome-screen"),
    navbar: document.getElementById("navbar"),
    mainWrapper: document.getElementById("main-wrapper"),
    appFooter: document.getElementById("app-footer"),

    // Welcome Screen Triggers
    welcomeBtnLogin: document.getElementById("welcome-btn-login"),
    welcomeBtnSignup: document.getElementById("welcome-btn-signup"),
    welcomeBtnGuest: document.getElementById("welcome-btn-guest"),
    welcomeQuickLoginBtn: document.getElementById("welcome-quick-login-btn"),

    // Theme Switchers
    themeToggleBtn: document.getElementById("theme-toggle-btn"),
    themeOptLight: document.getElementById("theme-opt-light"),
    themeOptDark: document.getElementById("theme-opt-dark"),
    authThemeToggleBtn: document.getElementById("auth-theme-toggle-btn"),
    authThemeOptLight: document.getElementById("auth-theme-opt-light"),
    authThemeOptDark: document.getElementById("auth-theme-opt-dark"),

    // Navbar Dropdowns
    guestProfileDropdown: document.getElementById("guest-profile-dropdown"),
    guestProfileBtn: document.getElementById("guest-profile-btn"),
    guestMenuSignin: document.getElementById("guest-menu-signin"),
    guestMenuSignup: document.getElementById("guest-menu-signup"),
    guestMenuExit: document.getElementById("guest-menu-exit"),

    userProfileDropdown: document.getElementById("user-profile-dropdown"),
    userProfileBtn: document.getElementById("user-profile-btn"),
    userNavAvatar: document.getElementById("user-nav-avatar"),
    userNavName: document.getElementById("user-nav-name"),
    userDropdownEmail: document.getElementById("user-dropdown-email"),
    menuMyProfile: document.getElementById("menu-my-profile"),
    menuWatchHistory: document.getElementById("menu-watch-history"),
    menuTasteProfile: document.getElementById("menu-taste-profile"),
    menuSettings: document.getElementById("menu-settings"),
    menuLogout: document.getElementById("menu-logout"),

    // Auth Modal Elements (Login / Signup / Forgot)
    authModal: document.getElementById("auth-modal"),
    authModalClose: document.getElementById("auth-modal-close"),
    tabBtnLogin: document.getElementById("tab-btn-login"),
    tabBtnSignup: document.getElementById("tab-btn-signup"),
    loginForm: document.getElementById("login-form"),
    signupForm: document.getElementById("signup-form"),
    forgotForm: document.getElementById("forgot-form"),
    loginEmail: document.getElementById("login-email"),
    loginPassword: document.getElementById("login-password"),
    toggleLoginPw: document.getElementById("toggle-login-pw"),
    btnLoginSubmit: document.getElementById("btn-login-submit"),
    btnLoginGuest: document.getElementById("btn-login-guest"),
    loginAlertError: document.getElementById("login-alert-error"),
    loginAlertSuccess: document.getElementById("login-alert-success"),
    signupName: document.getElementById("signup-name"),
    signupEmail: document.getElementById("signup-email"),
    signupPassword: document.getElementById("signup-password"),
    signupConfirmPassword: document.getElementById("signup-confirm-password"),
    toggleSignupPw: document.getElementById("toggle-signup-pw"),
    btnSignupSubmit: document.getElementById("btn-signup-submit"),
    btnSignupGuest: document.getElementById("btn-signup-guest"),
    signupAlertError: document.getElementById("signup-alert-error"),
    signupAlertSuccess: document.getElementById("signup-alert-success"),
    linkForgotPassword: document.getElementById("link-forgot-password"),
    linkSwitchToSignup: document.getElementById("link-switch-to-signup"),
    linkSwitchToLogin: document.getElementById("link-switch-to-login"),
    linkBackToLogin: document.getElementById("link-back-to-login"),
    forgotEmail: document.getElementById("forgot-email"),
    btnForgotSubmit: document.getElementById("btn-forgot-submit"),
    forgotAlertError: document.getElementById("forgot-alert-error"),
    forgotAlertSuccess: document.getElementById("forgot-alert-success"),

    // Guest Protected Feature Prompt Modal
    guestAuthPromptModal: document.getElementById("guest-auth-prompt-modal"),
    guestPromptClose: document.getElementById("guest-prompt-close"),
    guestPromptDesc: document.getElementById("guest-prompt-desc"),
    guestPromptLoginBtn: document.getElementById("guest-prompt-login-btn"),
    guestPromptSignupBtn: document.getElementById("guest-prompt-signup-btn"),
    guestPromptContinueBtn: document.getElementById("guest-prompt-continue-btn"),

    // User Profile Edit Modal
    userProfileModal: document.getElementById("user-profile-modal"),
    userModalClose: document.getElementById("user-modal-close"),
    profileAvatarCurrent: document.getElementById("profile-avatar-current"),
    profileModalName: document.getElementById("profile-modal-name"),
    profileModalEmail: document.getElementById("profile-modal-email"),
    profileEditForm: document.getElementById("profile-edit-form"),
    editProfileName: document.getElementById("edit-profile-name"),
    editProfileBio: document.getElementById("edit-profile-bio"),
    profileStatWatched: document.getElementById("profile-stat-watched"),
    profileStatRated: document.getElementById("profile-stat-rated"),
    btnProfileLogout: document.getElementById("btn-profile-logout"),

    // Hero Billboard
    heroSection: document.getElementById("hero"),
    heroBackdrop: document.getElementById("hero-backdrop"),
    heroAmbientGlow: document.getElementById("hero-ambient-glow"),
    heroTitle: document.getElementById("hero-title"),
    heroTagline: document.getElementById("hero-tagline"),
    heroRating: document.getElementById("hero-rating"),
    heroYear: document.getElementById("hero-year"),
    heroDuration: document.getElementById("hero-duration"),
    heroImdb: document.getElementById("hero-imdb"),
    heroGenres: document.getElementById("hero-genres"),
    heroDescription: document.getElementById("hero-description"),
    heroMatchScore: document.getElementById("hero-match-score"),
    heroReasonText: document.getElementById("hero-reason-text"),
    heroQuality: document.getElementById("hero-quality"),
    heroAudio: document.getElementById("hero-audio"),
    heroPlayBtn: document.getElementById("hero-play-btn"),
    heroInfoBtn: document.getElementById("hero-info-btn"),
    heroLikeBtn: document.getElementById("hero-like-btn"),
    heroWatchlistBtn: document.getElementById("hero-watchlist-btn"),
    heroCounter: document.getElementById("hero-counter"),
    heroDots: document.getElementById("hero-dots"),
    
    // Hero Showcase Card
    heroShowcasePoster: document.getElementById("hero-showcase-poster"),
    showcaseMatchBadge: document.getElementById("showcase-match-badge"),
    showcasePersonaTag: document.getElementById("showcase-persona-tag"),
    showcasePlayTrigger: document.getElementById("showcase-play-trigger"),
    heroQuickStars: document.getElementById("hero-quick-stars"),
    
    // Inline AI Prompt Bar
    aiPromptBarSection: document.querySelector(".ai-prompt-bar-section"),
    aiInlineForm: document.getElementById("ai-inline-form"),
    aiInlineInput: document.getElementById("ai-inline-input"),
    btnVoiceInput: document.getElementById("btn-voice-input"),
    quickPromptChips: document.getElementById("quick-prompt-chips"),
    
    // Search
    searchInput: document.getElementById("movie-search-input"),
    searchClearBtn: document.getElementById("search-clear-btn"),
    searchResultsSection: document.getElementById("search-results-section"),
    searchMovieGrid: document.getElementById("search-movie-grid"),
    searchQueryDisplay: document.getElementById("search-query-display"),
    btnCloseSearch: document.getElementById("btn-close-search"),
    
    // Persona Switcher
    personaDropdownContainer: document.getElementById("persona-dropdown-container"),
    personaBtn: document.getElementById("persona-btn"),
    personaMenu: document.getElementById("persona-menu"),
    personaList: document.getElementById("persona-list"),
    activePersonaAvatar: document.getElementById("active-persona-avatar"),
    activePersonaName: document.getElementById("active-persona-name"),
    
    // Onboarding Cold Start Banner
    coldStartBanner: document.getElementById("cold-start-banner"),
    btnOnboardingExplore: document.getElementById("btn-onboarding-explore"),

    // Carousels & Grids
    aiRecsHeading: document.getElementById("ai-recs-heading"),
    topRecsCarousel: document.getElementById("top-recs-carousel"),
    aiRecsSubtitle: document.getElementById("ai-recs-subtitle"),
    top10Carousel: document.getElementById("top-10-carousel"),
    becauseWatchedSection: document.getElementById("because-watched-section"),
    becauseWatchedCarousel: document.getElementById("because-watched-carousel"),
    becauseWatchedSource: document.getElementById("because-watched-source"),
    mindbendersCarousel: document.getElementById("mindbenders-carousel"),
    crimeCarousel: document.getElementById("crime-carousel"),
    fullCatalogGrid: document.getElementById("full-catalog-grid"),
    genreSelectDropdown: document.getElementById("genre-select-dropdown"),
    languageSelectDropdown: document.getElementById("language-select-dropdown"),
    industrySelectDropdown: document.getElementById("industry-select-dropdown"),
    countrySelectDropdown: document.getElementById("country-select-dropdown"),
    sortSelectDropdown: document.getElementById("sort-select-dropdown"),
    
    // Filters
    tasteFilterBar: document.querySelector(".taste-filter-bar"),
    moodChips: document.getElementById("mood-chips"),
    typeBtns: document.querySelectorAll(".type-btn"),
    
    // CineBot Chat
    floatingChatTrigger: document.getElementById("floating-chat-trigger"),
    navChatBtn: document.getElementById("nav-chat-btn"),
    chatDrawer: document.getElementById("chat-drawer"),
    chatExpandBtn: document.getElementById("chat-expand-btn"),
    chatCloseBtn: document.getElementById("chat-close-btn"),
    chatClearBtn: document.getElementById("chat-clear-btn"),
    chatMessages: document.getElementById("chat-messages"),
    chatSuggestions: document.getElementById("chat-suggestions"),
    chatInputForm: document.getElementById("chat-input-form"),
    chatInput: document.getElementById("chat-input"),
    chatMicBtn: document.getElementById("chat-mic-btn"),
    voiceRecordingIndicator: document.getElementById("voice-recording-indicator"),
    btnVoiceCancel: document.getElementById("btn-voice-cancel"),
    
    // Modals
    navTasteProfileBtn: document.getElementById("nav-taste-profile-btn"),
    tasteProfileModal: document.getElementById("taste-profile-modal"),
    tasteModalClose: document.getElementById("taste-modal-close"),
    modalUserAvatar: document.getElementById("modal-user-avatar"),
    modalUserName: document.getElementById("modal-user-name"),
    genreAffinityBars: document.getElementById("genre-affinity-bars"),
    modalMoodCloud: document.getElementById("modal-mood-cloud"),
    modalWatchedCount: document.getElementById("modal-watched-count"),
    modalHistoryList: document.getElementById("modal-history-list"),
    sliderAction: document.getElementById("slider-action"),
    sliderDark: document.getElementById("slider-dark"),
    sliderPlot: document.getElementById("slider-plot"),
    valAction: document.getElementById("val-action"),
    valDark: document.getElementById("val-dark"),
    valPlot: document.getElementById("val-plot"),
    btnSaveSliders: document.getElementById("btn-save-sliders"),
    btnResetProfile: document.getElementById("btn-reset-profile"),
    
    // Movie Detail Modal
    movieDetailModal: document.getElementById("movie-detail-modal"),
    movieModalClose: document.getElementById("movie-modal-close"),
    detailBackdrop: document.getElementById("detail-backdrop"),
    detailTitle: document.getElementById("detail-title"),
    detailTagline: document.getElementById("detail-tagline"),
    detailRating: document.getElementById("detail-rating"),
    detailYear: document.getElementById("detail-year"),
    detailDuration: document.getElementById("detail-duration"),
    detailImdb: document.getElementById("detail-imdb"),
    detailType: document.getElementById("detail-type"),
    detailMatchScore: document.getElementById("detail-match-score"),
    detailExplanationText: document.getElementById("detail-explanation-text"),
    detailDescription: document.getElementById("detail-description"),
    detailDirector: document.getElementById("detail-director"),
    detailCast: document.getElementById("detail-cast"),
    detailLanguage: document.getElementById("detail-language"),
    detailCountry: document.getElementById("detail-country"),
    detailGenres: document.getElementById("detail-genres"),
    detailMoodPills: document.getElementById("detail-mood-pills"),
    detailKeywordPills: document.getElementById("detail-keyword-pills"),
    detailStarButtons: document.getElementById("detail-star-buttons"),
    detailDislikeBtn: document.getElementById("detail-dislike-btn"),
    detailTrailerBtn: document.getElementById("detail-trailer-btn"),
    modalSimilarGrid: document.getElementById("modal-similar-grid"),
    
    // Video Trailer Player Modal
    trailerModal: document.getElementById("trailer-modal"),
    trailerModalClose: document.getElementById("trailer-modal-close"),
    trailerIframeContainer: document.getElementById("trailer-iframe-container"),
    trailerMovieTitle: document.getElementById("trailer-movie-title"),
    trailerMovieSub: document.getElementById("trailer-movie-sub"),
    
    // Footer Links
    footerLinkTaste: document.getElementById("footer-link-taste"),
    footerLinkCinebot: document.getElementById("footer-link-cinebot"),
    footerLinkSignin: document.getElementById("footer-link-signin"),
    footerLinkSignup: document.getElementById("footer-link-signup"),
    footerLinkHistory: document.getElementById("footer-link-history"),

    // Toast
    toast: document.getElementById("toast"),
    toastMsg: document.getElementById("toast-msg")
};

// ==========================================================================
// App Initialization & Theme System
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
    initThemeSystem();
    initApp();
    setupEventListeners();
});

function initThemeSystem() {
    let savedTheme = "dark";
    try {
        savedTheme = localStorage.getItem("cineflix-theme") || "dark";
    } catch (e) {
        console.warn("LocalStorage unavailable:", e);
    }
    applyTheme(savedTheme, false);
}

function applyTheme(theme, showFeedback = true) {
    state.theme = theme;
    document.documentElement.setAttribute("data-theme", theme);
    if (document.body) {
        document.body.classList.remove("netflix-dark", "netflix-light");
        document.body.classList.add(theme === "dark" ? "netflix-dark" : "netflix-light");
    }
    try {
        localStorage.setItem("cineflix-theme", theme);
    } catch (e) {}

    // Update main navbar toggle
    if (elements.themeOptLight && elements.themeOptDark) {
        if (theme === "light") {
            elements.themeOptLight.classList.add("active");
            elements.themeOptDark.classList.remove("active");
        } else {
            elements.themeOptDark.classList.add("active");
            elements.themeOptLight.classList.remove("active");
        }
    }

    // Update auth header toggle
    if (elements.authThemeOptLight && elements.authThemeOptDark) {
        if (theme === "light") {
            elements.authThemeOptLight.classList.add("active");
            elements.authThemeOptDark.classList.remove("active");
        } else {
            elements.authThemeOptDark.classList.add("active");
            elements.authThemeOptLight.classList.remove("active");
        }
    }

    if (showFeedback && typeof showToast === "function") {
        showToast(theme === "light" ? "☀️ Switched to Light Mode" : "🌙 Switched to Dark Mode");
    }
}

function toggleTheme() {
    const nextTheme = state.theme === "dark" ? "light" : "dark";
    applyTheme(nextTheme, true);
}

// ==========================================================================
// Centralized Authentication State Controller
// ==========================================================================

function setAuthState(newAuthState, user = null) {
    state.authState = newAuthState;
    
    if (newAuthState === "authenticated" && user) {
        state.isAuthenticated = true;
        state.isGuest = false;
        state.currentUser = user;
        sessionStorage.removeItem("cineflix_guest_active");

        if (elements.authHeader) elements.authHeader.style.display = "none";
        if (elements.authWelcomeScreen) elements.authWelcomeScreen.style.display = "none";
        if (elements.navbar) elements.navbar.style.display = "block";
        if (elements.mainWrapper) elements.mainWrapper.style.display = "block";
        if (elements.appFooter) elements.appFooter.style.display = "block";
        if (elements.floatingChatTrigger) elements.floatingChatTrigger.style.display = "flex";

        if (elements.guestProfileDropdown) elements.guestProfileDropdown.style.display = "none";
        if (elements.userProfileDropdown) {
            elements.userProfileDropdown.style.display = "block";
            if (elements.userNavAvatar) elements.userNavAvatar.innerText = user.avatar || "👤";
            if (elements.userNavName) elements.userNavName.innerText = user.name || "User";
            if (elements.userDropdownEmail) elements.userDropdownEmail.innerText = user.email || "";
        }
    } else if (newAuthState === "guest") {
        state.isAuthenticated = false;
        state.isGuest = true;
        state.currentUser = null;
        sessionStorage.setItem("cineflix_guest_active", "true");

        if (elements.authHeader) elements.authHeader.style.display = "none";
        if (elements.authWelcomeScreen) elements.authWelcomeScreen.style.display = "none";
        if (elements.navbar) elements.navbar.style.display = "block";
        if (elements.mainWrapper) elements.mainWrapper.style.display = "block";
        if (elements.appFooter) elements.appFooter.style.display = "block";
        if (elements.floatingChatTrigger) elements.floatingChatTrigger.style.display = "flex";

        if (elements.userProfileDropdown) elements.userProfileDropdown.style.display = "none";
        if (elements.guestProfileDropdown) elements.guestProfileDropdown.style.display = "block";
    } else {
        // Unauthenticated Welcome Screen
        state.authState = "unauthenticated";
        state.isAuthenticated = false;
        state.isGuest = false;
        state.currentUser = null;
        sessionStorage.removeItem("cineflix_guest_active");

        if (elements.authHeader) elements.authHeader.style.display = "flex";
        if (elements.authWelcomeScreen) elements.authWelcomeScreen.style.display = "flex";
        if (elements.navbar) elements.navbar.style.display = "none";
        if (elements.mainWrapper) elements.mainWrapper.style.display = "none";
        if (elements.appFooter) elements.appFooter.style.display = "none";
        if (elements.floatingChatTrigger) elements.floatingChatTrigger.style.display = "none";
        if (elements.userProfileDropdown) elements.userProfileDropdown.style.display = "none";
        if (elements.guestProfileDropdown) elements.guestProfileDropdown.style.display = "none";
    }
}

async function initApp() {
    const isAuth = await checkAuthStatus();
    if (isAuth) {
        // Active logged-in session exists
        await fetchPersonas();
        await fetchRecommendations();
        await fetchCatalog();
        initCuratedRows();
        initChatWelcome();
    } else if (sessionStorage.getItem("cineflix_guest_active") === "true") {
        // Active guest session
        setAuthState("guest");
        await fetchPersonas();
        await fetchRecommendations();
        await fetchCatalog();
        initCuratedRows();
        initChatWelcome();
    } else {
        // Unauthenticated initial user -> Show welcome screen
        setAuthState("unauthenticated");
        // Pre-fetch in background for instant responsiveness upon entering
        fetchCatalog().catch(() => {});
        fetchPersonas().catch(() => {});
        initCuratedRows();
        initChatWelcome();
    }
}

async function checkAuthStatus() {
    try {
        const res = await fetch("/api/auth/me");
        const data = await res.json();
        
        if (data.authenticated && data.user) {
            state.userProfile = data.profile;
            setAuthState("authenticated", data.user);
            return true;
        } else {
            state.userProfile = data.profile;
            return false;
        }
    } catch (err) {
        console.error("Error checking auth status:", err);
        return false;
    }
}

function continueAsGuest() {
    setAuthState("guest");
    closeAuthModal();
    if (elements.guestAuthPromptModal) {
        elements.guestAuthPromptModal.classList.remove("open");
    }
    showToast("🍿 Browsing CineFlix as Guest");
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (!state.recommendations || state.recommendations.length === 0) {
        fetchRecommendations();
    }
    if (!state.allMovies || state.allMovies.length === 0) {
        fetchCatalog();
    }
    initChatWelcome();
}

// Protected Action Interceptor
function requireAuth(actionName = "access this feature") {
    if (state.authState === "authenticated") return true;
    
    if (elements.guestPromptDesc) {
        elements.guestPromptDesc.innerText = `Sign in or create a free account to ${actionName}, save your viewing history, and receive personalized AI recommendations.`;
    }
    if (elements.guestAuthPromptModal) {
        elements.guestAuthPromptModal.classList.add("open");
    }
    return false;
}

// ==========================================================================
// Authentication Modal Logic (Login / Signup / Forgot Password)
// ==========================================================================

function openAuthModal(tab = "login") {
    switchAuthTab(tab);
    clearAuthAlerts();
    elements.authModal.classList.add("open");
}

function closeAuthModal() {
    elements.authModal.classList.remove("open");
    clearAuthAlerts();
}

function switchAuthTab(tab) {
    clearAuthAlerts();
    if (tab === "login") {
        elements.tabBtnLogin.classList.add("active");
        elements.tabBtnSignup.classList.remove("active");
        elements.loginForm.style.display = "flex";
        elements.signupForm.style.display = "none";
        elements.forgotForm.style.display = "none";
    } else if (tab === "signup") {
        elements.tabBtnSignup.classList.add("active");
        elements.tabBtnLogin.classList.remove("active");
        elements.signupForm.style.display = "flex";
        elements.loginForm.style.display = "none";
        elements.forgotForm.style.display = "none";
    } else if (tab === "forgot") {
        elements.tabBtnLogin.classList.remove("active");
        elements.tabBtnSignup.classList.remove("active");
        elements.forgotForm.style.display = "flex";
        elements.loginForm.style.display = "none";
        elements.signupForm.style.display = "none";
    }
}

function clearAuthAlerts() {
    [elements.loginAlertError, elements.loginAlertSuccess, 
     elements.signupAlertError, elements.signupAlertSuccess,
     elements.forgotAlertError, elements.forgotAlertSuccess].forEach(el => {
        if (el) {
            el.style.display = "none";
            el.innerText = "";
        }
    });
}

async function handleLogin(e) {
    e.preventDefault();
    clearAuthAlerts();
    
    const email = elements.loginEmail.value.trim();
    const password = elements.loginPassword.value;
    const btn = elements.btnLoginSubmit;
    const spinner = btn.querySelector(".btn-spinner");
    const btnText = btn.querySelector(".btn-text");

    if (!email || !password) {
        showAuthAlert(elements.loginAlertError, "Please enter your email and password.");
        return;
    }

    try {
        btn.disabled = true;
        if (spinner) spinner.style.display = "inline-block";
        if (btnText) btnText.style.opacity = "0.7";

        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();

        if (res.ok && data.success) {
            setAuthState("authenticated", data.user);
            showToast(`🍿 Welcome back, ${data.user.name}!`);
            closeAuthModal();
            if (elements.guestAuthPromptModal) elements.guestAuthPromptModal.classList.remove("open");
            elements.loginForm.reset();
            await fetchRecommendations();
            await fetchPersonas();
            window.scrollTo({ top: 0, behavior: "smooth" });
        } else {
            showAuthAlert(elements.loginAlertError, data.error || "Invalid email or password.");
        }
    } catch (err) {
        showAuthAlert(elements.loginAlertError, "Network connection error. Please try again.");
    } finally {
        btn.disabled = false;
        if (spinner) spinner.style.display = "none";
        if (btnText) btnText.style.opacity = "1";
    }
}

async function handleSignup(e) {
    e.preventDefault();
    clearAuthAlerts();

    const name = elements.signupName.value.trim();
    const email = elements.signupEmail.value.trim();
    const password = elements.signupPassword.value;
    const confirmPw = elements.signupConfirmPassword.value;
    const btn = elements.btnSignupSubmit;
    const spinner = btn.querySelector(".btn-spinner");
    const btnText = btn.querySelector(".btn-text");

    if (password !== confirmPw) {
        showAuthAlert(elements.signupAlertError, "Passwords do not match. Please re-enter.");
        return;
    }

    if (password.length < 6) {
        showAuthAlert(elements.signupAlertError, "Password must be at least 6 characters long.");
        return;
    }

    try {
        btn.disabled = true;
        if (spinner) spinner.style.display = "inline-block";
        if (btnText) btnText.style.opacity = "0.7";

        const res = await fetch("/api/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password, avatar: "👤" })
        });
        const data = await res.json();

        if (res.ok && data.success) {
            setAuthState("authenticated", data.user);
            showToast(`🎉 Welcome to CineFlix, ${data.user.name}!`);
            closeAuthModal();
            if (elements.guestAuthPromptModal) elements.guestAuthPromptModal.classList.remove("open");
            elements.signupForm.reset();
            await fetchRecommendations();
            await fetchPersonas();
            window.scrollTo({ top: 0, behavior: "smooth" });
        } else {
            showAuthAlert(elements.signupAlertError, data.error || "Unable to register account.");
        }
    } catch (err) {
        showAuthAlert(elements.signupAlertError, "Network connection error. Please try again.");
    } finally {
        btn.disabled = false;
        if (spinner) spinner.style.display = "none";
        if (btnText) btnText.style.opacity = "1";
    }
}

async function handleLogout() {
    try {
        await fetch("/api/auth/logout", { method: "POST" });
    } catch (err) {
        console.error("Logout error:", err);
    }
    setAuthState("unauthenticated");
    if (elements.userProfileDropdown) elements.userProfileDropdown.classList.remove("open");
    if (elements.guestProfileDropdown) elements.guestProfileDropdown.classList.remove("open");
    window.scrollTo({ top: 0, behavior: "smooth" });
    showToast("👋 You have been logged out.");
}

async function handleForgotPassword(e) {
    e.preventDefault();
    clearAuthAlerts();
    const email = elements.forgotEmail.value.trim();

    if (!email) {
        showAuthAlert(elements.forgotAlertError, "Please enter your registered email address.");
        return;
    }

    try {
        const res = await fetch("/api/auth/forgot-password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });
        const data = await res.json();
        if (res.ok) {
            showAuthAlert(elements.forgotAlertSuccess, data.message || "Reset link dispatched.");
            elements.forgotEmail.value = "";
        } else {
            showAuthAlert(elements.forgotAlertError, data.error || "Error processing request.");
        }
    } catch (err) {
        showAuthAlert(elements.forgotAlertError, "Error connecting to server.");
    }
}

function showAuthAlert(element, message) {
    if (!element) return;
    element.innerText = message;
    element.style.display = "block";
}

// User Profile View Modal
function openUserProfileModal() {
    if (!requireAuth("view your profile")) return;
    
    const user = state.currentUser;
    if (!user) return;

    elements.profileAvatarCurrent.innerText = user.avatar || "👤";
    elements.profileModalName.innerText = user.name;
    elements.profileModalEmail.innerText = user.email;
    elements.editProfileName.value = user.name;
    elements.editProfileBio.value = user.bio || "";

    const stats = state.userProfile && state.userProfile.stats ? state.userProfile.stats : {};
    elements.profileStatWatched.innerText = `${stats.watched_count || 0} Watched`;
    elements.profileStatRated.innerText = `${stats.rated_count || 0} Rated`;

    elements.userProfileModal.classList.add("open");
    elements.userProfileDropdown.classList.remove("open");
}

async function handleSaveProfile(e) {
    e.preventDefault();
    const name = elements.editProfileName.value.trim();
    const bio = elements.editProfileBio.value.trim();
    const avatar = elements.profileAvatarCurrent.innerText;

    try {
        const res = await fetch("/api/auth/update-profile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, bio, avatar })
        });
        const data = await res.json();
        if (res.ok && data.success) {
            state.currentUser = data.user;
            if (elements.userNavName) elements.userNavName.innerText = data.user.name;
            if (elements.userNavAvatar) elements.userNavAvatar.innerText = data.user.avatar;
            showToast("✨ Profile details saved!");
            elements.userProfileModal.classList.remove("open");
            await fetchRecommendations();
        }
    } catch (err) {
        console.error("Profile update error:", err);
    }
}

// ==========================================================================
// Event Listeners Setup
// ==========================================================================

function setupEventListeners() {
    // Theme Switcher Listeners (Navbar)
    if (elements.themeToggleBtn) {
        elements.themeToggleBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const lightTarget = e.target.closest("#theme-opt-light");
            const darkTarget = e.target.closest("#theme-opt-dark");
            if (lightTarget) {
                applyTheme("light", true);
            } else if (darkTarget) {
                applyTheme("dark", true);
            } else {
                toggleTheme();
            }
        });
    }

    // Theme Switcher Listeners (Auth Header)
    if (elements.authThemeToggleBtn) {
        elements.authThemeToggleBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const lightTarget = e.target.closest("#auth-theme-opt-light");
            const darkTarget = e.target.closest("#auth-theme-opt-dark");
            if (lightTarget) {
                applyTheme("light", true);
            } else if (darkTarget) {
                applyTheme("dark", true);
            } else {
                toggleTheme();
            }
        });
    }

    // Navbar Scroll Effect
    window.addEventListener("scroll", () => {
        if (elements.navbar && window.scrollY > 40) {
            elements.navbar.classList.add("scrolled");
        } else if (elements.navbar) {
            elements.navbar.classList.remove("scrolled");
        }
    });

    // Welcome Screen Buttons
    if (elements.welcomeBtnLogin) elements.welcomeBtnLogin.addEventListener("click", () => openAuthModal("login"));
    if (elements.welcomeBtnSignup) elements.welcomeBtnSignup.addEventListener("click", () => openAuthModal("signup"));
    if (elements.welcomeBtnGuest) elements.welcomeBtnGuest.addEventListener("click", continueAsGuest);
    if (elements.welcomeQuickLoginBtn) elements.welcomeQuickLoginBtn.addEventListener("click", () => openAuthModal("login"));

    // Modal & Form Triggers
    if (elements.authModalClose) elements.authModalClose.addEventListener("click", closeAuthModal);
    if (elements.tabBtnLogin) elements.tabBtnLogin.addEventListener("click", () => switchAuthTab("login"));
    if (elements.tabBtnSignup) elements.tabBtnSignup.addEventListener("click", () => switchAuthTab("signup"));
    if (elements.loginForm) elements.loginForm.addEventListener("submit", handleLogin);
    if (elements.signupForm) elements.signupForm.addEventListener("submit", handleSignup);
    if (elements.forgotForm) elements.forgotForm.addEventListener("submit", handleForgotPassword);
    if (elements.linkForgotPassword) elements.linkForgotPassword.addEventListener("click", (e) => { e.preventDefault(); switchAuthTab("forgot"); });
    if (elements.linkSwitchToSignup) elements.linkSwitchToSignup.addEventListener("click", (e) => { e.preventDefault(); switchAuthTab("signup"); });
    if (elements.linkSwitchToLogin) elements.linkSwitchToLogin.addEventListener("click", (e) => { e.preventDefault(); switchAuthTab("login"); });
    if (elements.linkBackToLogin) elements.linkBackToLogin.addEventListener("click", (e) => { e.preventDefault(); switchAuthTab("login"); });
    if (elements.btnLoginGuest) elements.btnLoginGuest.addEventListener("click", continueAsGuest);
    if (elements.btnSignupGuest) elements.btnSignupGuest.addEventListener("click", continueAsGuest);

    // Guest Protected Prompt Modal Listeners
    if (elements.guestPromptClose) elements.guestPromptClose.addEventListener("click", () => elements.guestAuthPromptModal.classList.remove("open"));
    if (elements.guestPromptLoginBtn) elements.guestPromptLoginBtn.addEventListener("click", () => {
        elements.guestAuthPromptModal.classList.remove("open");
        openAuthModal("login");
    });
    if (elements.guestPromptSignupBtn) elements.guestPromptSignupBtn.addEventListener("click", () => {
        elements.guestAuthPromptModal.classList.remove("open");
        openAuthModal("signup");
    });
    if (elements.guestPromptContinueBtn) elements.guestPromptContinueBtn.addEventListener("click", () => {
        elements.guestAuthPromptModal.classList.remove("open");
    });

    // Guest Profile Navbar Dropdown
    if (elements.guestProfileBtn) {
        elements.guestProfileBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            elements.guestProfileDropdown.classList.toggle("open");
        });
    }
    if (elements.guestMenuSignin) elements.guestMenuSignin.addEventListener("click", (e) => {
        e.preventDefault();
        elements.guestProfileDropdown.classList.remove("open");
        openAuthModal("login");
    });
    if (elements.guestMenuSignup) elements.guestMenuSignup.addEventListener("click", (e) => {
        e.preventDefault();
        elements.guestProfileDropdown.classList.remove("open");
        openAuthModal("signup");
    });
    if (elements.guestMenuExit) elements.guestMenuExit.addEventListener("click", (e) => {
        e.preventDefault();
        elements.guestProfileDropdown.classList.remove("open");
        handleLogout();
    });

    // Demo Account Pills
    document.querySelectorAll(".demo-pill").forEach(pill => {
        pill.addEventListener("click", () => {
            elements.loginEmail.value = pill.dataset.email;
            elements.loginPassword.value = pill.dataset.pw;
            elements.btnLoginSubmit.click();
        });
    });

    // Show/Hide Password toggles
    if (elements.toggleLoginPw) {
        elements.toggleLoginPw.addEventListener("click", () => {
            const isPw = elements.loginPassword.type === "password";
            elements.loginPassword.type = isPw ? "text" : "password";
            elements.toggleLoginPw.innerHTML = isPw ? '<i class="fa-solid fa-eye-slash"></i>' : '<i class="fa-solid fa-eye"></i>';
        });
    }
    if (elements.toggleSignupPw) {
        elements.toggleSignupPw.addEventListener("click", () => {
            const isPw = elements.signupPassword.type === "password";
            elements.signupPassword.type = isPw ? "text" : "password";
            elements.toggleSignupPw.innerHTML = isPw ? '<i class="fa-solid fa-eye-slash"></i>' : '<i class="fa-solid fa-eye"></i>';
        });
    }

    // User Profile Dropdown
    if (elements.userProfileBtn) {
        elements.userProfileBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            elements.userProfileDropdown.classList.toggle("open");
        });
    }
    if (elements.menuMyProfile) elements.menuMyProfile.addEventListener("click", (e) => { e.preventDefault(); openUserProfileModal(); });
    if (elements.menuWatchHistory) elements.menuWatchHistory.addEventListener("click", (e) => { e.preventDefault(); if (!requireAuth("view your viewing history")) return; openTasteProfileModal(); });
    if (elements.menuTasteProfile) elements.menuTasteProfile.addEventListener("click", (e) => { e.preventDefault(); if (!requireAuth("view your personalized Taste Profile")) return; openTasteProfileModal(); });
    if (elements.menuSettings) elements.menuSettings.addEventListener("click", (e) => { e.preventDefault(); if (!requireAuth("access settings & sliders")) return; openTasteProfileModal(); });
    if (elements.menuLogout) elements.menuLogout.addEventListener("click", (e) => { e.preventDefault(); handleLogout(); });

    // User Profile Edit Modal
    if (elements.userModalClose) elements.userModalClose.addEventListener("click", () => elements.userProfileModal.classList.remove("open"));
    if (elements.profileEditForm) elements.profileEditForm.addEventListener("submit", handleSaveProfile);
    if (elements.btnProfileLogout) elements.btnProfileLogout.addEventListener("click", () => { elements.userProfileModal.classList.remove("open"); handleLogout(); });

    // Avatar selector
    document.querySelectorAll(".avatar-opt").forEach(opt => {
        opt.addEventListener("click", () => {
            elements.profileAvatarCurrent.innerText = opt.dataset.avatar;
        });
    });

    // Persona dropdown
    if (elements.personaBtn) {
        elements.personaBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            elements.personaBtn.parentElement.classList.toggle("open");
        });
    }
    document.addEventListener("click", () => {
        if (elements.personaBtn) elements.personaBtn.parentElement.classList.remove("open");
        if (elements.userProfileDropdown) elements.userProfileDropdown.classList.remove("open");
        if (elements.guestProfileDropdown) elements.guestProfileDropdown.classList.remove("open");
    });

    // Search Input with Debounce
    let searchDebounce = null;
    elements.searchInput.addEventListener("input", (e) => {
        const query = e.target.value.trim();
        elements.searchClearBtn.style.display = query ? "block" : "none";
        clearTimeout(searchDebounce);
        searchDebounce = setTimeout(() => {
            handleSearch(query);
        }, 200);
    });

    elements.searchClearBtn.addEventListener("click", () => {
        clearSearch();
    });

    elements.btnCloseSearch.addEventListener("click", () => {
        clearSearch();
    });

    // Inline AI Prompt Form
    elements.aiInlineForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const query = elements.aiInlineInput.value.trim();
        if (!query) return;
        openChatDrawer();
        sendUserMessage(query);
        elements.aiInlineInput.value = "";
    });

    // Quick Prompt Chips
    elements.quickPromptChips.querySelectorAll(".quick-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const query = chip.dataset.query;
            openChatDrawer();
            sendUserMessage(query);
        });
    });

    // Onboarding Explore Button
    if (elements.btnOnboardingExplore) {
        elements.btnOnboardingExplore.addEventListener("click", () => {
            const cat = document.getElementById("categories-section");
            if (cat) cat.scrollIntoView({ behavior: "smooth" });
        });
    }

    // Mood Filters
    elements.moodChips.querySelectorAll(".mood-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            elements.moodChips.querySelectorAll(".mood-chip").forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            state.activeMood = chip.dataset.mood;
            fetchRecommendations();
        });
    });

    // Type Filter (All, Movie, TV Show)
    elements.typeBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            elements.typeBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            state.activeType = btn.dataset.type;
            if (state.searchQuery) {
                handleSearch(state.searchQuery);
            } else {
                fetchRecommendations();
                fetchCatalog();
            }
        });
    });

    // Catalog Dropdowns
    if (elements.genreSelectDropdown) {
        elements.genreSelectDropdown.addEventListener("change", (e) => {
            state.activeGenre = e.target.value;
            if (state.searchQuery) {
                handleSearch(state.searchQuery);
            } else {
                fetchCatalog();
            }
        });
    }
    if (elements.languageSelectDropdown) {
        elements.languageSelectDropdown.addEventListener("change", (e) => {
            state.activeLanguage = e.target.value;
            if (state.searchQuery) {
                handleSearch(state.searchQuery);
            } else {
                fetchCatalog();
            }
        });
    }
    if (elements.industrySelectDropdown) {
        elements.industrySelectDropdown.addEventListener("change", (e) => {
            state.activeIndustry = e.target.value;
            if (state.searchQuery) {
                handleSearch(state.searchQuery);
            } else {
                fetchCatalog();
            }
        });
    }
    if (elements.countrySelectDropdown) {
        elements.countrySelectDropdown.addEventListener("change", (e) => {
            state.activeCountry = e.target.value;
            if (state.searchQuery) {
                handleSearch(state.searchQuery);
            } else {
                fetchCatalog();
            }
        });
    }
    if (elements.sortSelectDropdown) {
        elements.sortSelectDropdown.addEventListener("change", (e) => {
            state.activeSort = e.target.value;
            if (state.searchQuery) {
                handleSearch(state.searchQuery);
            } else {
                fetchCatalog();
            }
        });
    }

    // CineBot Chat Trigger & Drawer
    if (elements.floatingChatTrigger) elements.floatingChatTrigger.addEventListener("click", toggleChatDrawer);
    if (elements.navChatBtn) elements.navChatBtn.addEventListener("click", openChatDrawer);
    if (elements.chatCloseBtn) elements.chatCloseBtn.addEventListener("click", toggleChatDrawer);
    if (elements.chatClearBtn) elements.chatClearBtn.addEventListener("click", clearChat);
    if (elements.chatExpandBtn) {
        elements.chatExpandBtn.addEventListener("click", () => {
            if (elements.chatDrawer) elements.chatDrawer.classList.toggle("fullscreen");
        });
    }

    // Taste Profile Nav Button
    if (elements.navTasteProfileBtn) {
        elements.navTasteProfileBtn.addEventListener("click", (e) => {
            e.preventDefault();
            if (!requireAuth("view your personalized Taste Profile")) return;
            openTasteProfileModal();
        });
    }

    // Footer Links
    if (elements.footerLinkTaste) {
        elements.footerLinkTaste.addEventListener("click", (e) => {
            e.preventDefault();
            if (!requireAuth("view your personalized Taste Profile")) return;
            openTasteProfileModal();
        });
    }
    if (elements.footerLinkHistory) {
        elements.footerLinkHistory.addEventListener("click", (e) => {
            e.preventDefault();
            if (!requireAuth("view your viewing history")) return;
            openTasteProfileModal();
        });
    }
    if (elements.footerLinkCinebot) elements.footerLinkCinebot.addEventListener("click", (e) => { e.preventDefault(); openChatDrawer(); });
    if (elements.footerLinkSignin) elements.footerLinkSignin.addEventListener("click", (e) => { e.preventDefault(); openAuthModal("login"); });
    if (elements.footerLinkSignup) elements.footerLinkSignup.addEventListener("click", (e) => { e.preventDefault(); openAuthModal("signup"); });

    if (elements.chatInputForm) {
        elements.chatInputForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const text = elements.chatInput ? elements.chatInput.value.trim() : "";
            if (!text) return;
            if (elements.chatInput) elements.chatInput.value = "";
            sendUserMessage(text);
        });
    }

    // Voice Input Trigger
    if (elements.btnVoiceInput) {
        elements.btnVoiceInput.addEventListener("click", () => {
            openChatDrawer();
            startVoiceRecognition();
        });
    }
    if (elements.chatMicBtn) {
        elements.chatMicBtn.addEventListener("click", startVoiceRecognition);
    }
    if (elements.btnVoiceCancel) {
        elements.btnVoiceCancel.addEventListener("click", stopVoiceRecognition);
    }

    if (recognition) {
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            stopVoiceRecognition();
            sendUserMessage(transcript);
        };
        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
            stopVoiceRecognition();
            showToast("⚠️ Voice input could not recognize speech. Please try typing!");
        };
        recognition.onend = () => {
            stopVoiceRecognition();
        };
    }

    // Taste Profile Modal
    if (elements.tasteModalClose) {
        elements.tasteModalClose.addEventListener("click", () => {
            if (elements.tasteProfileModal) elements.tasteProfileModal.classList.remove("open");
        });
    }
    if (elements.btnSaveSliders) elements.btnSaveSliders.addEventListener("click", saveSliders);
    if (elements.btnResetProfile) elements.btnResetProfile.addEventListener("click", resetProfile);

    // Slider inputs live display
    if (elements.sliderAction) elements.sliderAction.addEventListener("input", (e) => { if (elements.valAction) elements.valAction.innerText = `${e.target.value}%`; });
    if (elements.sliderDark) elements.sliderDark.addEventListener("input", (e) => { if (elements.valDark) elements.valDark.innerText = `${e.target.value}%`; });
    if (elements.sliderPlot) elements.sliderPlot.addEventListener("input", (e) => { if (elements.valPlot) elements.valPlot.innerText = `${e.target.value}%`; });

    // Movie Detail Modal
    if (elements.movieModalClose) {
        elements.movieModalClose.addEventListener("click", () => {
            if (elements.movieDetailModal) elements.movieDetailModal.classList.remove("open");
        });
    }

    // Star rating buttons in modal
    if (elements.detailStarButtons) {
        elements.detailStarButtons.querySelectorAll(".star-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                if (!requireAuth("rate this title")) return;
                const rating = parseInt(btn.dataset.rating);
                rateMovie(state.selectedMovieId, rating);
            });
        });
    }

    if (elements.detailDislikeBtn) {
        elements.detailDislikeBtn.addEventListener("click", () => {
            if (!requireAuth("dislike this title")) return;
            dislikeMovie(state.selectedMovieId);
        });
    }

    if (elements.detailTrailerBtn) {
        elements.detailTrailerBtn.addEventListener("click", () => {
            const movie = recommenderFind(state.selectedMovieId);
            if (movie) openTrailerModal(movie);
        });
    }

    // Trailer Modal Close
    if (elements.trailerModalClose) elements.trailerModalClose.addEventListener("click", closeTrailerModal);

    // Hero Billboard Actions
    elements.heroPlayBtn.addEventListener("click", () => {
        if (state.heroSlides.length > 0) {
            const movie = state.heroSlides[state.activeHeroIndex];
            openTrailerModal(movie);
        }
    });

    elements.heroInfoBtn.addEventListener("click", () => {
        if (state.heroSlides.length > 0) {
            const movie = state.heroSlides[state.activeHeroIndex];
            openMovieDetail(movie.id);
        }
    });

    elements.heroLikeBtn.addEventListener("click", () => {
        if (!requireAuth("rate this title")) return;
        if (state.heroSlides.length > 0) {
            const movie = state.heroSlides[state.activeHeroIndex];
            rateMovie(movie.id, 5);
        }
    });

    elements.heroWatchlistBtn.addEventListener("click", () => {
        if (!requireAuth("save to watchlist")) return;
        if (state.heroSlides.length > 0) {
            const movie = state.heroSlides[state.activeHeroIndex];
            rateMovie(movie.id, 4);
            showToast(`Added ${movie.title} to your Watchlist!`);
        }
    });

    // Hero Dots
    elements.heroDots.querySelectorAll(".hero-dot").forEach((dot, index) => {
        dot.addEventListener("click", () => {
            showHeroSlide(index);
            startHeroAutoRotation();
        });
    });

    // Hero 3D Card Play Trigger
    elements.showcasePlayTrigger.addEventListener("click", () => {
        if (state.heroSlides.length > 0) {
            const movie = state.heroSlides[state.activeHeroIndex];
            openTrailerModal(movie);
        }
    });

    // Hero Quick Stars
    elements.heroQuickStars.querySelectorAll("i").forEach(star => {
        star.addEventListener("click", () => {
            if (!requireAuth("rate this title")) return;
            if (state.heroSlides.length > 0) {
                const r = parseInt(star.dataset.rating);
                const movie = state.heroSlides[state.activeHeroIndex];
                rateMovie(movie.id, r);
                updateHeroQuickStars(r);
                showToast(`Rated ${movie.title} ${'★'.repeat(r)}!`);
            }
        });
    });

    // Carousel Navigation Arrows
    document.querySelectorAll(".carousel-arrow").forEach(arrow => {
        arrow.addEventListener("click", () => {
            const targetId = arrow.dataset.target;
            const carousel = document.getElementById(targetId);
            if (!carousel) return;
            const scrollAmount = carousel.clientWidth * 0.75;
            if (arrow.classList.contains("prev")) {
                carousel.scrollBy({ left: -scrollAmount, behavior: "smooth" });
            } else {
                carousel.scrollBy({ left: scrollAmount, behavior: "smooth" });
            }
        });
    });

    // Footer Links
    if (elements.footerLinkTaste) elements.footerLinkTaste.addEventListener("click", (e) => { e.preventDefault(); openTasteProfileModal(); });
    if (elements.footerLinkCinebot) elements.footerLinkCinebot.addEventListener("click", (e) => { e.preventDefault(); openChatDrawer(); });
    if (elements.footerLinkSignin) elements.footerLinkSignin.addEventListener("click", (e) => { e.preventDefault(); openAuthModal("login"); });
    if (elements.footerLinkSignup) elements.footerLinkSignup.addEventListener("click", (e) => { e.preventDefault(); openAuthModal("signup"); });
    if (elements.footerLinkHistory) elements.footerLinkHistory.addEventListener("click", (e) => { e.preventDefault(); openTasteProfileModal(); });
}

// Helper to find movie from loaded state
function recommenderFind(movieId) {
    if (state.allMovies) {
        const found = state.allMovies.find(m => m.id === movieId);
        if (found) return found;
    }
    if (state.recommendations) {
        const found = state.recommendations.find(m => m.id === movieId);
        if (found) return found;
    }
    return null;
}

// ==========================================================================
// API Handlers
// ==========================================================================

async function fetchPersonas() {
    try {
        const res = await fetch("/api/personas");
        const data = await res.json();
        renderPersonas(data.personas);
    } catch (err) {
        console.error("Error fetching personas:", err);
    }
}

async function selectPersona(personaId) {
    try {
        const res = await fetch("/api/personas/select", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ persona_id: personaId })
        });
        const data = await res.json();
        state.activePersona = personaId;
        showToast(`Applied persona: ${data.profile.name}`);
        await checkAuthStatus();
        await fetchPersonas();
        await fetchRecommendations();
    } catch (err) {
        console.error("Error selecting persona:", err);
    }
}

async function fetchRecommendations() {
    try {
        const reqBody = {
            top_n: 12,
            type: state.activeType === "All" ? null : state.activeType,
            genre: (state.activeMood !== "all" && !["Mind-bending", "Dark", "Feel-Good", "Non-Stop Action", "Wholesome", "Visually Stunning"].includes(state.activeMood)) ? state.activeMood : null
        };

        const res = await fetch("/api/recommendations", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(reqBody)
        });
        const data = await res.json();
        
        state.recommendations = data.recommendations;
        state.becauseWatched = data.because_you_watched;
        state.userProfile = data.user_profile;
        state.isColdStart = data.is_cold_start;

        // Setup Section Title & Subtitle
        if (state.authState === "guest" || state.isGuest) {
            if (elements.coldStartBanner) elements.coldStartBanner.style.display = "none";
            elements.aiRecsHeading.innerHTML = `<span class="title-highlight">🔥 Popular Picks for You</span> on Netflix`;
            elements.aiRecsSubtitle.innerText = "Top-rated and critically acclaimed Netflix favorites";
        } else if (data.is_cold_start) {
            if (elements.coldStartBanner) elements.coldStartBanner.style.display = "block";
            elements.aiRecsHeading.innerHTML = `<span class="title-highlight">🌟 Popular Picks</span> on Netflix`;
            elements.aiRecsSubtitle.innerText = "Trending titles with high critical acclaim. Rate titles to unlock your personalized AI radar.";
        } else {
            if (elements.coldStartBanner) elements.coldStartBanner.style.display = "none";
            elements.aiRecsHeading.innerHTML = `<span class="title-highlight">🔥 Top AI Recommendations</span> for You`;
            const stats = (data.user_profile && data.user_profile.stats) ? data.user_profile.stats : {};
            const userName = (data.user_profile && data.user_profile.name) ? data.user_profile.name : "You";
            elements.aiRecsSubtitle.innerText = `Personalized for ${userName} (${stats.watched_count || 0} watched, ${stats.rated_count || 0} rated)`;
        }

        // Setup Hero Billboard Top 5 Slides
        if (data.recommendations && data.recommendations.length > 0) {
            state.heroSlides = data.recommendations.slice(0, 5);
            showHeroSlide(0);
            startHeroAutoRotation();
        }

        // Render Top AI Carousel
        renderMovieCarousel(elements.topRecsCarousel, data.recommendations);

        // Render "Because You Watched" Row
        if (data.because_you_watched) {
            elements.becauseWatchedSection.style.display = "block";
            elements.becauseWatchedSource.innerText = data.because_you_watched.source_movie.title;
            renderMovieCarousel(elements.becauseWatchedCarousel, data.because_you_watched.recommendations);
        } else {
            elements.becauseWatchedSection.style.display = "none";
        }

    } catch (err) {
        console.error("Error fetching recommendations:", err);
    }
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function clearSearch() {
    state.searchQuery = "";
    if (elements.searchInput) elements.searchInput.value = "";
    if (elements.searchClearBtn) elements.searchClearBtn.style.display = "none";
    if (elements.searchResultsSection) elements.searchResultsSection.style.display = "none";
    if (elements.heroSection) elements.heroSection.style.display = "";
    if (elements.aiPromptBarSection) elements.aiPromptBarSection.style.display = "";
    if (elements.tasteFilterBar) elements.tasteFilterBar.style.display = "";
}

function populateGenreDropdown(genres) {
    if (!elements.genreSelectDropdown || !genres) return;
    const current = state.activeGenre || "All";
    elements.genreSelectDropdown.innerHTML = `<option value="All">All Genres</option>`;
    genres.forEach(g => {
        const opt = document.createElement("option");
        opt.value = g;
        opt.innerText = g;
        if (g === current) opt.selected = true;
        elements.genreSelectDropdown.appendChild(opt);
    });
}

function populateLanguageDropdown(languages) {
    if (!elements.languageSelectDropdown || !languages) return;
    const current = state.activeLanguage || "All";
    elements.languageSelectDropdown.innerHTML = `<option value="All">All Languages</option>`;
    languages.forEach(l => {
        const opt = document.createElement("option");
        opt.value = l;
        opt.innerText = l;
        if (l === current) opt.selected = true;
        elements.languageSelectDropdown.appendChild(opt);
    });
}

function populateIndustryDropdown(industries) {
    if (!elements.industrySelectDropdown || !industries) return;
    const current = state.activeIndustry || "All";
    elements.industrySelectDropdown.innerHTML = `<option value="All">All Industries</option>`;
    industries.forEach(ind => {
        const opt = document.createElement("option");
        opt.value = ind;
        opt.innerText = ind;
        if (ind === current) opt.selected = true;
        elements.industrySelectDropdown.appendChild(opt);
    });
}

function populateCountryDropdown(countries) {
    if (!elements.countrySelectDropdown || !countries) return;
    const current = state.activeCountry || "All";
    elements.countrySelectDropdown.innerHTML = `<option value="All">All Countries</option>`;
    countries.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.innerText = c;
        if (c === current) opt.selected = true;
        elements.countrySelectDropdown.appendChild(opt);
    });
}

async function fetchCatalog() {
    try {
        const queryParams = new URLSearchParams({
            genre: state.activeGenre || "All",
            language: state.activeLanguage || "All",
            industry: state.activeIndustry || "All",
            country: state.activeCountry || "All",
            type: state.activeType || "All",
            sort: state.activeSort || "default",
            limit: 150
        });
        const res = await fetch(`/api/movies?${queryParams.toString()}`);
        const data = await res.json();
        
        state.allMovies = data.movies;
        state.genres = data.genres;
        
        if (data.genres) populateGenreDropdown(data.genres);
        if (data.languages) populateLanguageDropdown(data.languages);
        if (data.industries) populateIndustryDropdown(data.industries);
        if (data.countries) populateCountryDropdown(data.countries);
        renderMovieGrid(elements.fullCatalogGrid, data.movies);
    } catch (err) {
        console.error("Error fetching catalog:", err);
    }
}

async function handleSearch(query) {
    state.searchQuery = query ? query.trim() : "";
    
    if (!state.searchQuery) {
        clearSearch();
        return;
    }
    
    // When searching, hide hero billboard & prompt bars so search results are front and center
    if (elements.heroSection) elements.heroSection.style.display = "none";
    if (elements.aiPromptBarSection) elements.aiPromptBarSection.style.display = "none";
    if (elements.tasteFilterBar) elements.tasteFilterBar.style.display = "none";
    if (elements.searchResultsSection) elements.searchResultsSection.style.display = "block";
    if (elements.searchQueryDisplay) elements.searchQueryDisplay.innerText = state.searchQuery;
    
    try {
        const queryParams = new URLSearchParams({
            search: state.searchQuery,
            genre: state.activeGenre || "All",
            language: state.activeLanguage || "All",
            industry: state.activeIndustry || "All",
            country: state.activeCountry || "All",
            type: state.activeType || "All",
            sort: state.activeSort || "default",
            limit: 150
        });
        const res = await fetch(`/api/movies?${queryParams.toString()}`);
        const data = await res.json();
        
        if (data.genres) populateGenreDropdown(data.genres);
        if (data.languages) populateLanguageDropdown(data.languages);
        if (data.industries) populateIndustryDropdown(data.industries);
        if (data.countries) populateCountryDropdown(data.countries);

        const searchResultsMeta = document.getElementById("search-results-meta");
        if (searchResultsMeta) {
            searchResultsMeta.innerText = `Found ${data.total} matching title${data.total === 1 ? '' : 's'} across Netflix India catalog`;
        }

        if (!data.movies || data.movies.length === 0) {
            elements.searchMovieGrid.innerHTML = `
                <div class="no-search-results" style="grid-column: 1/-1; text-align: center; padding: 4rem 2rem; background: var(--bg-card); border-radius: 16px; border: 1px dashed var(--border-color); margin: 1rem 0;">
                    <div style="font-size: 3.5rem; color: var(--primary-accent); margin-bottom: 1rem;"><i class="fa-solid fa-film"></i></div>
                    <h3 style="font-size: 1.4rem; margin-bottom: 0.6rem; color: var(--text-primary); font-weight: 700;">No results found for "${escapeHtml(state.searchQuery)}"</h3>
                    <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 540px; margin: 0 auto; line-height: 1.6;">Try searching for a title, actor, director, genre, language, or mood (e.g., "Marathi", "3 Idiots", "Christopher Nolan", "Hindi Thriller", "Aamir Khan", "Sairat").</p>
                </div>
            `;
        } else {
            renderMovieGrid(elements.searchMovieGrid, data.movies);
        }
    } catch (err) {
        console.error("Error searching movies:", err);
    }
}


async function rateMovie(movieId, rating) {
    if (!requireAuth("rate this title")) return;

    try {
        const res = await fetch("/api/profile/interact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "rate", movie_id: movieId, rating: rating })
        });
        const data = await res.json();
        showToast(data.message);
        updateModalStarDisplay(rating);
        await checkAuthStatus();
        await fetchRecommendations();
    } catch (err) {
        console.error("Error rating movie:", err);
    }
}

async function dislikeMovie(movieId) {
    if (!requireAuth("dislike this title")) return;

    try {
        const res = await fetch("/api/profile/interact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "dislike", movie_id: movieId })
        });
        const data = await res.json();
        showToast("Marked as not interested. CineFlix won't recommend this again.");
        elements.movieDetailModal.classList.remove("open");
        await checkAuthStatus();
        await fetchRecommendations();
    } catch (err) {
        console.error("Error disliking movie:", err);
    }
}

async function saveSliders() {
    if (!requireAuth("tune your taste sliders")) return;

    try {
        const sliders = {
            action_level: parseInt(elements.sliderAction.value),
            dark_tone: parseInt(elements.sliderDark.value),
            plot_depth: parseInt(elements.sliderPlot.value)
        };
        await fetch("/api/profile/sliders", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(sliders)
        });
        showToast("Taste sliders updated! Recomputing recommendations...");
        await fetchRecommendations();
    } catch (err) {
        console.error("Error saving sliders:", err);
    }
}

async function resetProfile() {
    if (!requireAuth("reset your profile")) return;
    if (!confirm("Reset your taste profile back to a clean slate?")) return;
    try {
        await fetch("/api/profile/reset", { method: "POST" });
        showToast("Profile reset to clean state.");
        elements.tasteProfileModal.classList.remove("open");
        await checkAuthStatus();
        await fetchPersonas();
        await fetchRecommendations();
    } catch (err) {
        console.error("Error resetting profile:", err);
    }
}

// ==========================================================================
// Curated Rows & Top 10 Today
// ==========================================================================
async function initCuratedRows() {
    try {
        // Top 10 on Netflix Today
        const resTop10 = await fetch("/api/movies?sort=imdb&limit=10");
        const dataTop10 = await resTop10.json();
        renderTop10Carousel(dataTop10.movies);

        // Mind-Benders row
        const res1 = await fetch("/api/movies?genre=Sci-Fi&limit=8");
        const data1 = await res1.json();
        renderMovieCarousel(elements.mindbendersCarousel, data1.movies);

        // Crime row
        const res2 = await fetch("/api/movies?genre=Crime&limit=8");
        const data2 = await res2.json();
        renderMovieCarousel(elements.crimeCarousel, data2.movies);
    } catch (err) {
        console.error("Error rendering curated rows:", err);
    }
}

function renderTop10Carousel(movies) {
    elements.top10Carousel.innerHTML = "";
    movies.forEach((movie, index) => {
        const rank = index + 1;
        const wrapper = document.createElement("div");
        wrapper.className = "top-10-card-wrapper";
        
        const rankNum = document.createElement("span");
        rankNum.className = "top-10-rank-num";
        rankNum.innerText = rank;

        const card = createMovieCard(movie);
        
        wrapper.appendChild(rankNum);
        wrapper.appendChild(card);
        elements.top10Carousel.appendChild(wrapper);
    });
}

// ==========================================================================
// Hero Billboard Slider & Showcase
// ==========================================================================

function showHeroSlide(index) {
    if (!state.heroSlides || state.heroSlides.length === 0) return;
    state.activeHeroIndex = index % state.heroSlides.length;
    const movie = state.heroSlides[state.activeHeroIndex];

    elements.heroTitle.innerText = movie.title;
    elements.heroTagline.innerText = movie.tagline ? `"${movie.tagline}"` : "";
    elements.heroRating.innerText = movie.rating || "TV-MA";
    elements.heroYear.innerText = movie.releaseYear || movie.release_year || "";
    elements.heroDuration.innerText = movie.duration || "";
    elements.heroImdb.innerText = movie.imdb_score || 8.0;
    elements.heroGenres.innerText = movie.genres ? movie.genres.join(", ") : "";
    elements.heroDescription.innerText = movie.description || "";

    const matchScore = movie.match_score || 95;
    const matchLabel = state.isColdStart ? `${matchScore}% Fit` : `${matchScore}% Match`;
    elements.heroMatchScore.innerText = matchLabel;
    elements.heroReasonText.innerText = movie.explanation || `Top-tier ${movie.genres ? movie.genres[0] : 'Netflix'} selection tailored to your taste profile.`;
    elements.heroQuality.innerText = movie.quality || "4K Ultra HD";
    elements.heroAudio.innerText = movie.audio || "Dolby Atmos";
    elements.heroCounter.innerText = `0${state.activeHeroIndex + 1} / 0${state.heroSlides.length}`;

    // Update backdrop artwork
    const backdropImg = movie.backdrop || movie.backdrop_url || movie.poster || movie.poster_url;
    if (backdropImg) {
        elements.heroBackdrop.style.backgroundImage = `url('${backdropImg}')`;
    } else if (movie.poster_bg) {
        elements.heroBackdrop.style.backgroundImage = "none";
        elements.heroBackdrop.style.background = movie.poster_bg;
    }

    // Update Showcase 3D Card
    const posterImg = movie.poster || movie.poster_url || movie.backdrop || movie.backdrop_url;
    if (posterImg) {
        elements.heroShowcasePoster.style.backgroundImage = `url('${posterImg}')`;
    } else {
        elements.heroShowcasePoster.style.background = movie.poster_bg || "linear-gradient(135deg, #111, #333)";
    }
    elements.showcaseMatchBadge.innerText = matchLabel;
    
    const userName = (state.currentUser && state.currentUser.name) 
        ? state.currentUser.name.split(" ")[0] 
        : (state.userProfile ? state.userProfile.name.split(" ")[0] : "Your");
    elements.showcasePersonaTag.innerText = `${userName}'s Taste`;

    // Update Dots
    const dots = elements.heroDots.querySelectorAll(".hero-dot");
    dots.forEach((d, i) => {
        if (i === state.activeHeroIndex) d.classList.add("active");
        else d.classList.remove("active");
    });
}

function startHeroAutoRotation() {
    clearInterval(state.heroTimer);
    state.heroTimer = setInterval(() => {
        if (!elements.movieDetailModal.classList.contains("open") && 
            !elements.trailerModal.classList.contains("open") &&
            !elements.authModal.classList.contains("open")) {
            showHeroSlide(state.activeHeroIndex + 1);
        }
    }, 7000);
}

function updateHeroQuickStars(rating) {
    const stars = elements.heroQuickStars.querySelectorAll("i");
    stars.forEach((s, idx) => {
        if (idx < rating) s.classList.add("active");
        else s.classList.remove("active");
    });
}

// ==========================================================================
// Video Trailer Modal
// ==========================================================================

function openTrailerModal(movie) {
    const releaseYear = movie.releaseYear || movie.release_year || "";
    const genresStr = movie.genres ? movie.genres.join(", ") : "";
    elements.trailerMovieTitle.innerText = `${movie.title} — Official Trailer`;
    elements.trailerMovieSub.innerText = `${releaseYear}${genresStr ? ' • ' + genresStr : ''} • ⭐ ${movie.imdb_score || 8.0} IMDb`;

    let trailerId = movie.trailer_id;
    if (!trailerId && movie.trailerUrl) {
        if (movie.trailerUrl.includes("v=")) {
            trailerId = movie.trailerUrl.split("v=")[1].split("&")[0];
        } else if (movie.trailerUrl.includes("youtu.be/")) {
            trailerId = movie.trailerUrl.split("youtu.be/")[1].split("?")[0];
        }
    }

    if (trailerId) {
        elements.trailerIframeContainer.innerHTML = `
            <iframe 
                src="https://www.youtube.com/embed/${trailerId}?autoplay=1&rel=0&modestbranding=1" 
                title="${movie.title} Trailer" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        `;
    } else {
        elements.trailerIframeContainer.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 320px; background: #0b0f19; color: #fff; text-align: center; padding: 2rem;">
                <i class="fa-solid fa-film" style="font-size: 3rem; color: var(--primary-accent); margin-bottom: 1rem;"></i>
                <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem;">Official Trailer Currently Unavailable</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 420px; line-height: 1.5;">Streaming rights or YouTube preview is not linked for "${escapeHtml(movie.title)}" (${releaseYear}). You can explore related titles in CineFlix!</p>
            </div>
        `;
    }

    elements.trailerModal.classList.add("open");
}

function closeTrailerModal() {
    elements.trailerIframeContainer.innerHTML = "";
    elements.trailerModal.classList.remove("open");
}

// ==========================================================================
// Voice Speech-To-Text Recognition
// ==========================================================================

function startVoiceRecognition() {
    if (!recognition) return;
    try {
        state.isVoiceRecording = true;
        elements.voiceRecordingIndicator.style.display = "flex";
        recognition.start();
        showToast("🎙️ Listening... Speak your movie preference now!");
    } catch (e) {
        console.log("Voice already running or error:", e);
    }
}

function stopVoiceRecognition() {
    state.isVoiceRecording = false;
    elements.voiceRecordingIndicator.style.display = "none";
    if (recognition) {
        try { recognition.stop(); } catch(e){}
    }
}

// ==========================================================================
// UI Renderers & Component Factories
// ==========================================================================

function renderPersonas(personas) {
    if (!elements.personaList) return;
    elements.personaList.innerHTML = "";
    personas.forEach(p => {
        if (p.is_active) {
            elements.activePersonaAvatar.innerText = p.avatar;
            elements.activePersonaName.innerText = p.name.split(" ")[0];
        }

        const div = document.createElement("div");
        div.className = `persona-item ${p.is_active ? "active" : ""}`;
        div.innerHTML = `
            <span class="persona-avatar">${p.avatar}</span>
            <div>
                <div class="persona-item-title">${p.name}</div>
                <div class="persona-item-desc">${p.description}</div>
            </div>
        `;
        div.addEventListener("click", () => {
            elements.personaBtn.parentElement.classList.remove("open");
            selectPersona(p.id);
        });
        elements.personaList.appendChild(div);
    });
}

function renderMovieCarousel(container, movies) {
    container.innerHTML = "";
    if (!movies || movies.length === 0) {
        container.innerHTML = `<p style="color: var(--text-muted); padding: 1rem;">No titles found.</p>`;
        return;
    }

    movies.forEach(movie => {
        const card = createMovieCard(movie);
        container.appendChild(card);
    });
}

function renderMovieGrid(container, movies) {
    container.innerHTML = "";
    if (!movies || movies.length === 0) {
        container.innerHTML = `<p style="color: var(--text-muted); grid-column: 1/-1; padding: 2rem;">No titles match your query.</p>`;
        return;
    }

    movies.forEach(movie => {
        const card = createMovieCard(movie);
        container.appendChild(card);
    });
}

function createMovieCard(movie) {
    const card = document.createElement("div");
    card.className = "movie-card";
    
    const posterImg = movie.poster || movie.poster_url || movie.backdrop || movie.backdrop_url;
    const bgStyle = posterImg ? `url('${posterImg}')` : (movie.poster_bg || "linear-gradient(135deg, #1f2937, #111827)");
    const matchScore = movie.match_score || Math.floor(75 + (movie.imdb_score || 7) * 2.5);
    const badgeLabel = movie.is_cold_start ? `${matchScore}% Fit` : `${matchScore}% Match`;
    const mainGenre = movie.genres && movie.genres.length ? movie.genres[0] : "Netflix";
    const vibeTag = movie.mood_tags && movie.mood_tags.length ? movie.mood_tags[0] : (movie.industry || "Popular");
    const explanation = movie.explanation || `Highly acclaimed ${mainGenre} with ${movie.imdb_score || 8.0} IMDb rating.`;
    const releaseYear = movie.releaseYear || movie.release_year || "";
    const langInfo = [movie.language, movie.country || movie.industry].filter(Boolean).join(" • ");

    card.innerHTML = `
        <div class="card-poster" style="background-image: ${bgStyle.startsWith('url') ? bgStyle : 'none'}; background: ${!bgStyle.startsWith('url') ? bgStyle : ''};">
            <div class="card-top-badges">
                <span class="match-badge">${badgeLabel}</span>
                <span class="type-pill">${movie.type || "Movie"}</span>
            </div>
            <div class="card-poster-title">${movie.title}</div>
        </div>
        <div class="card-body">
            <div class="card-meta-line">
                <span>${releaseYear}${langInfo ? ' • ' + langInfo : ''}</span>
                <span class="card-imdb"><i class="fa-solid fa-star"></i> ${movie.imdb_score || 8.0}</span>
            </div>
            <div class="card-genres">${movie.genres ? movie.genres.join(", ") : ""}</div>
            <div class="card-vibe-tag">${vibeTag}</div>
            <div class="card-explanation">${explanation}</div>
        </div>
    `;

    card.addEventListener("click", () => openMovieDetail(movie.id));
    return card;
}

// ==========================================================================
// Movie Detail Preview Modal
// ==========================================================================

async function openMovieDetail(movieId) {
    state.selectedMovieId = movieId;
    try {
        const res = await fetch(`/api/movie/${movieId}`);
        const data = await res.json();
        const movie = data.movie;
        const similar = data.similar_movies;

        elements.detailTitle.innerText = movie.title;
        elements.detailTagline.innerText = movie.tagline ? `"${movie.tagline}"` : "";
        elements.detailRating.innerText = movie.rating || "TV-MA";
        elements.detailYear.innerText = movie.releaseYear || movie.release_year || "";
        elements.detailDuration.innerText = movie.duration || "";
        elements.detailImdb.innerText = movie.imdb_score || 8.0;
        elements.detailType.innerText = movie.type || "Movie";
        elements.detailDescription.innerText = movie.description || "";
        elements.detailDirector.innerText = movie.director || "Unknown";
        elements.detailCast.innerText = movie.cast ? movie.cast.join(", ") : "Various";
        if (elements.detailLanguage) elements.detailLanguage.innerText = movie.language || "Hindi / English";
        if (elements.detailCountry) elements.detailCountry.innerText = `${movie.country || 'India'} (${movie.industry || 'Cinema'})`;
        elements.detailGenres.innerText = movie.genres ? movie.genres.join(", ") : "";

        // Match Score & AI Reason
        const matchPct = movie.match_score || 95;
        elements.detailMatchScore.innerText = `${matchPct}% Match`;
        elements.detailExplanationText.innerText = movie.explanation || `Recommended because of its strong thematic resonance with your top-rated picks and ${movie.genres ? movie.genres[0] : 'cinematic'} storytelling.`;

        const backdropImg = movie.backdrop || movie.backdrop_url || movie.poster || movie.poster_url;
        if (backdropImg) {
            elements.detailBackdrop.style.backgroundImage = `url('${backdropImg}')`;
        } else {
            elements.detailBackdrop.style.background = movie.poster_bg || "linear-gradient(135deg, #111, #333)";
        }

        // Mood Pills
        elements.detailMoodPills.innerHTML = "";
        (movie.mood_tags || []).forEach(m => {
            const span = document.createElement("span");
            span.className = "tag-pill";
            span.innerText = m;
            elements.detailMoodPills.appendChild(span);
        });

        // Keywords
        elements.detailKeywordPills.innerHTML = "";
        (movie.keywords || []).forEach(k => {
            const span = document.createElement("span");
            span.className = "tag-pill";
            span.innerText = `#${k}`;
            elements.detailKeywordPills.appendChild(span);
        });

        // User Rating state
        const userRating = (state.userProfile && state.userProfile.stats && state.userProfile.stats.watched_movies)
            ? (state.userProfile.stats.watched_movies.find(m => m.id === movieId)?.user_rating || 0)
            : 0;
        updateModalStarDisplay(userRating);

        // Similar Grid
        renderModalSimilarMovies(similar);

        elements.movieDetailModal.classList.add("open");
    } catch (err) {
        console.error("Error opening movie detail:", err);
    }
}

function updateModalStarDisplay(rating) {
    const starBtns = elements.detailStarButtons.querySelectorAll(".star-btn");
    starBtns.forEach(btn => {
        const starVal = parseInt(btn.dataset.rating);
        if (starVal <= rating) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    });
}

function renderModalSimilarMovies(similar) {
    elements.modalSimilarGrid.innerHTML = "";
    if (!similar || similar.length === 0) {
        elements.modalSimilarGrid.innerHTML = `<p style="color: var(--text-muted);">No similar titles found.</p>`;
        return;
    }

    similar.forEach(m => {
        const item = document.createElement("div");
        item.className = "chat-movie-card";
        const thumb = m.poster_url || m.backdrop_url;
        item.innerHTML = `
            <div class="chat-movie-thumb" style="background-image: url('${thumb}');"></div>
            <div class="chat-movie-info">
                <div class="chat-movie-title">${m.title}</div>
                <div class="chat-movie-meta">${m.release_year} • ${m.genres[0]} • ⭐ ${m.imdb_score}</div>
            </div>
            <span class="chat-movie-score">${m.match_score || 95}%</span>
        `;
        item.addEventListener("click", () => openMovieDetail(m.id));
        elements.modalSimilarGrid.appendChild(item);
    });
}

// ==========================================================================
// Taste Profile Modal
// ==========================================================================

async function openTasteProfileModal() {
    try {
        const res = await fetch("/api/profile");
        const data = await res.json();
        const profile = data.profile;
        const stats = data.stats;

        const userName = (state.currentUser && state.currentUser.name) ? state.currentUser.name : (profile.name || "Your");
        const userAvatar = (state.currentUser && state.currentUser.avatar) ? state.currentUser.avatar : (profile.avatar || "🚀");

        elements.modalUserAvatar.innerText = userAvatar;
        elements.modalUserName.innerText = `${userName}'s Taste Profile`;
        elements.modalWatchedCount.innerText = stats.watched_count || 0;

        // Genre affinity bars
        elements.genreAffinityBars.innerHTML = "";
        if (stats.genre_distribution && stats.genre_distribution.length > 0) {
            stats.genre_distribution.forEach(g => {
                const div = document.createElement("div");
                div.className = "genre-bar-item";
                div.innerHTML = `
                    <div class="genre-bar-labels">
                        <span>${g.genre}</span>
                        <span>${g.pct}% (${g.count} titles)</span>
                    </div>
                    <div class="genre-bar-track">
                        <div class="genre-bar-fill" style="width: ${g.pct}%;"></div>
                    </div>
                `;
                elements.genreAffinityBars.appendChild(div);
            });
        } else {
            elements.genreAffinityBars.innerHTML = `<p style="color: var(--text-muted); font-size: 0.85rem;">Rate movies in the catalog to build your genre affinity breakdown.</p>`;
        }

        // Mood tag cloud
        elements.modalMoodCloud.innerHTML = "";
        if (stats.top_moods && stats.top_moods.length > 0) {
            stats.top_moods.forEach(m => {
                const span = document.createElement("span");
                span.className = "mood-cloud-tag";
                span.innerText = `${m.mood} (${m.count})`;
                elements.modalMoodCloud.appendChild(span);
            });
        } else {
            elements.modalMoodCloud.innerHTML = `<span style="color: var(--text-muted); font-size: 0.85rem;">No mood vibes recorded yet.</span>`;
        }

        // Sliders
        const sliders = stats.sliders || {};
        elements.sliderAction.value = sliders.action_level || 50;
        elements.sliderDark.value = sliders.dark_tone || 50;
        elements.sliderPlot.value = sliders.plot_depth || 50;
        elements.valAction.innerText = (sliders.action_level || 50) + "%";
        elements.valDark.innerText = (sliders.dark_tone || 50) + "%";
        elements.valPlot.innerText = (sliders.plot_depth || 50) + "%";

        // History list
        elements.modalHistoryList.innerHTML = "";
        if (!stats.watched_movies || stats.watched_movies.length === 0) {
            elements.modalHistoryList.innerHTML = `<p style="color: var(--text-muted); padding: 1rem;">No viewing history yet. Rate titles to shape your profile!</p>`;
        } else {
            stats.watched_movies.forEach(m => {
                const item = document.createElement("div");
                item.className = "history-item";
                const ratingStr = m.user_rating ? "★".repeat(m.user_rating) : "Watched";
                item.innerHTML = `
                    <div class="history-item-info">
                        <div class="history-title">${m.title} (${m.release_year})</div>
                        <div class="history-rating">${ratingStr} • ${m.genres.join(", ")}</div>
                    </div>
                    <button class="btn-text-danger" data-id="${m.id}"><i class="fa-solid fa-trash"></i></button>
                `;
                item.querySelector("button").addEventListener("click", async (e) => {
                    e.stopPropagation();
                    await fetch("/api/profile/interact", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ action: "unwatch", movie_id: m.id })
                    });
                    openTasteProfileModal();
                    fetchRecommendations();
                });
                elements.modalHistoryList.appendChild(item);
            });
        }

        elements.tasteProfileModal.classList.add("open");
    } catch (err) {
        console.error("Error opening taste profile modal:", err);
    }
}

// ==========================================================================
// CineBot AI Conversational Curator & Interactive Preference Engine
// ==========================================================================

const CINEBOT_LANGUAGES = [
    { label: "All Languages", value: "All" },
    { label: "Hindi", value: "Hindi" },
    { label: "English", value: "English" },
    { label: "Marathi", value: "Marathi" },
    { label: "Tamil", value: "Tamil" },
    { label: "Telugu", value: "Telugu" },
    { label: "Malayalam", value: "Malayalam" },
    { label: "Kannada", value: "Kannada" },
    { label: "Korean", value: "Korean" },
    { label: "Japanese", value: "Japanese" },
    { label: "Spanish", value: "Spanish" }
];

const CINEBOT_CINEMAS = [
    { label: "All Cinema", value: "All" },
    { label: "Bollywood", value: "Bollywood" },
    { label: "Marathi Cinema", value: "Marathi Cinema" },
    { label: "Hollywood", value: "Hollywood" },
    { label: "South Indian", value: "South Indian" },
    { label: "Korean", value: "Korean" },
    { label: "Japanese", value: "Japanese" },
    { label: "International", value: "International" }
];

const CINEBOT_GENRES = [
    { label: "Romance", value: "Romance" },
    { label: "Comedy", value: "Comedy" },
    { label: "Action", value: "Action" },
    { label: "Horror", value: "Horror" },
    { label: "Thriller", value: "Thriller" },
    { label: "Mystery", value: "Mystery" },
    { label: "Drama", value: "Drama" },
    { label: "Sci-Fi", value: "Sci-Fi" },
    { label: "Fantasy", value: "Fantasy" },
    { label: "Crime", value: "Crime" },
    { label: "Feel-Good", value: "Feel-Good" },
    { label: "Any Genre", value: "Any Genre" }
];

const CINEBOT_YEARS = [
    { label: "Any Year", value: "Any Year" },
    { label: "Latest Releases", value: "Latest Releases" },
    { label: "2026", value: "2026" },
    { label: "2025", value: "2025" },
    { label: "2024", value: "2024" },
    { label: "2023", value: "2023" },
    { label: "2022", value: "2022" },
    { label: "2021", value: "2021" },
    { label: "2020", value: "2020" },
    { label: "2010s", value: "2010s" },
    { label: "2000s", value: "2000s" },
    { label: "1990s", value: "1990s" },
    { label: "1980s", value: "1980s" }
];

const CINEBOT_TYPES = [
    { label: "All / Both", value: "Both" },
    { label: "Movies", value: "Movie" },
    { label: "TV Series", value: "TV Show" }
];

const CINEBOT_DURATIONS = [
    { label: "Any Duration", value: "Any Duration" },
    { label: "Under 90 min", value: "Under 90 min" },
    { label: "90–120 min", value: "90–120 min" },
    { label: "120–150 min", value: "120–150 min" },
    { label: "150+ min", value: "150+ min" }
];

const CINEBOT_QUICK_SUGGESTIONS = [
    "Hindi Romance",
    "Bollywood Comedy",
    "Marathi Horror",
    "Hollywood Thriller",
    "English Sci-Fi",
    "Korean",
    "TV Series",
    "Any Language"
];

let cinebotPreferences = {
    language: null,
    cinema: null,
    genres: [],
    year: null,
    type: null,
    duration: null
};

function toggleChatDrawer() {
    const drawer = elements.chatDrawer || document.getElementById("chat-drawer");
    if (!drawer) return;
    drawer.classList.toggle("open");
    if (drawer.classList.contains("open")) {
        initializeCineBot();
        if (elements.chatInput) elements.chatInput.focus();
    }
}

function openChatDrawer() {
    const drawer = elements.chatDrawer || document.getElementById("chat-drawer");
    if (!drawer) return;
    drawer.classList.add("open");
    initializeCineBot();
    if (elements.chatInput) elements.chatInput.focus();
}

function clearChat() {
    initializeCineBot(true);
}

function initChatWelcome() {
    initializeCineBot(false);
}

/**
 * Initializes CineBot with the welcome flow and preference options.
 * Does NOT require an API call to display the initial options.
 */
function initializeCineBot(forceReset = false) {
    const container = elements.chatMessages || document.getElementById("chat-messages");
    if (!container) return;

    if (!forceReset && container.children.length > 0) {
        return;
    }

    container.innerHTML = "";
    cinebotPreferences = {
        language: null,
        cinema: null,
        genres: [],
        year: null,
        type: null,
        duration: null
    };
    state.chatContext = {};

    // 1. Initial Welcome Message Sequence & Language Question
    const welcomeHtml = `
        <div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 6px;">Hi! I'm CineBot AI 👋</div>
        <div style="font-weight: 700; color: var(--accent-cyan); margin-top: 6px;">Which language do you prefer?</div>
    `;

    renderBotOptionsMessage(welcomeHtml, CINEBOT_LANGUAGES, (item, btn, group) => {
        handleLanguageSelection(item, btn, group);
    });

    renderChatSuggestions(CINEBOT_QUICK_SUGGESTIONS);
}

/**
 * Step 1 -> Step 2: Language Selection Handler
 */
function handleLanguageSelection(item, btn, group) {
    highlightSelectedChip(btn, group);
    cinebotPreferences.language = item.value;

    renderUserMessage(item.label);

    showBotTyping(300, () => {
        const botHtml = `
            <div style="font-weight: 700; color: var(--accent-cyan);">Which cinema do you prefer?</div>
        `;

        renderBotOptionsMessage(botHtml, CINEBOT_CINEMAS, (cinemaItem, cBtn, cGroup) => {
            handleCinemaSelection(cinemaItem, cBtn, cGroup);
        });
    });
}

/**
 * Step 2 -> Step 3: Cinema Selection Handler
 */
function handleCinemaSelection(item, btn, group) {
    highlightSelectedChip(btn, group);
    cinebotPreferences.cinema = item.value;

    renderUserMessage(item.label);

    showBotTyping(300, () => {
        const botHtml = `
            <div style="font-weight: 700; color: var(--accent-cyan);">What are you in the mood for?</div>
        `;

        renderBotOptionsMessage(botHtml, CINEBOT_GENRES, (genreItem, gBtn, gGroup) => {
            handleGenreSelection(genreItem, gBtn, gGroup);
        });
    });
}

/**
 * Step 3 -> Step 4: Genre / Mood Selection Handler
 */
function handleGenreSelection(item, btn, group) {
    highlightSelectedChip(btn, group);
    cinebotPreferences.genres = [item.value];

    renderUserMessage(item.label);

    showBotTyping(300, () => {
        const botHtml = `
            <div style="font-weight: 700; color: var(--accent-cyan);">What year are you interested in?</div>
        `;

        renderBotOptionsMessage(botHtml, CINEBOT_YEARS, (yearItem, yBtn, yGroup) => {
            handleYearSelection(yearItem, yBtn, yGroup);
        });
    });
}

/**
 * Step 4 -> Step 5: Year Selection Handler
 */
function handleYearSelection(item, btn, group) {
    highlightSelectedChip(btn, group);
    cinebotPreferences.year = item.value;

    renderUserMessage(item.label);

    showBotTyping(300, () => {
        const botHtml = `
            <div style="font-weight: 700; color: var(--accent-cyan);">What do you want to watch?</div>
        `;

        renderBotOptionsMessage(botHtml, CINEBOT_TYPES, (typeItem, tBtn, tGroup) => {
            handleTypeSelection(typeItem, tBtn, tGroup);
        });
    });
}

/**
 * Step 5 -> Step 6: Type Selection Handler
 */
function handleTypeSelection(item, btn, group) {
    highlightSelectedChip(btn, group);
    cinebotPreferences.type = item.value;

    renderUserMessage(item.label);

    showBotTyping(300, () => {
        const botHtml = `
            <div style="font-weight: 700; color: var(--accent-cyan); margin-bottom: 4px;">How much time do you have?</div>
            <div style="font-size: 0.76rem; color: var(--text-muted);">Pick preferred duration or skip:</div>
        `;

        renderBotDurationMessage(botHtml, CINEBOT_DURATIONS, (durItem) => {
            handleDurationSelection(durItem);
        });
    });
}

/**
 * Step 6 -> Step 7: Duration Selection & Summary Display
 */
function handleDurationSelection(item) {
    cinebotPreferences.duration = item ? item.value : "Any Duration";
    renderUserMessage(item ? item.label : "Any Duration");

    showBotTyping(300, () => {
        renderPreferencesSummary();
    });
}

/**
 * Step 7: Render Final Watch Preferences Summary Card
 */
function renderPreferencesSummary() {
    const langDisplay = cinebotPreferences.language || "All Languages";
    const cinemaDisplay = cinebotPreferences.cinema || "All Cinema";
    const genreDisplay = (cinebotPreferences.genres && cinebotPreferences.genres.length > 0 && !cinebotPreferences.genres.includes("Any"))
        ? cinebotPreferences.genres.join(", ")
        : "Any Genre";
    const yearDisplay = cinebotPreferences.year || "Any Year";
    const typeDisplay = cinebotPreferences.type === "Movie" ? "Movies" : (cinebotPreferences.type === "TV Show" ? "TV Series" : "All / Both");
    const durDisplay = cinebotPreferences.duration || "Any Duration";

    const msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg bot";

    const summaryCardHtml = `
        <div class="msg-bubble" style="width: 100%;">
            <div style="margin-bottom: 8px; font-weight: 800; font-size: 0.96rem;">✨ Your Watch Preferences</div>
            <div class="chat-summary-card">
                <div class="chat-summary-grid">
                    <div class="chat-summary-item">
                        <span class="chat-summary-label">Language</span>
                        <span class="chat-summary-val">${escapeHtml(langDisplay)}</span>
                    </div>
                    <div class="chat-summary-item">
                        <span class="chat-summary-label">Cinema</span>
                        <span class="chat-summary-val">${escapeHtml(cinemaDisplay)}</span>
                    </div>
                    <div class="chat-summary-item">
                        <span class="chat-summary-label">Mood / Genre</span>
                        <span class="chat-summary-val">${escapeHtml(genreDisplay)}</span>
                    </div>
                    <div class="chat-summary-item">
                        <span class="chat-summary-label">Year</span>
                        <span class="chat-summary-val">${escapeHtml(yearDisplay)}</span>
                    </div>
                    <div class="chat-summary-item">
                        <span class="chat-summary-label">Type</span>
                        <span class="chat-summary-val">${escapeHtml(typeDisplay)}</span>
                    </div>
                    <div class="chat-summary-item">
                        <span class="chat-summary-label">Duration</span>
                        <span class="chat-summary-val">${escapeHtml(durDisplay)}</span>
                    </div>
                </div>
            </div>
            <div class="chat-action-bar" style="margin-top: 14px;">
                <button class="chat-btn-confirm" id="btn-chat-find-movies">
                    <i class="fa-solid fa-clapperboard"></i> Find My Movies
                </button>
                <button class="chat-btn-secondary" id="btn-chat-edit-pref">
                    <i class="fa-solid fa-pen-to-square"></i> Edit Preferences
                </button>
                <button class="chat-btn-secondary" id="btn-chat-reset-pref">
                    <i class="fa-solid fa-rotate-left"></i> Reset
                </button>
            </div>
        </div>
    `;

    msgDiv.innerHTML = summaryCardHtml;

    // Attach click listeners to summary card buttons
    const findBtn = msgDiv.querySelector("#btn-chat-find-movies");
    const editBtn = msgDiv.querySelector("#btn-chat-edit-pref");
    const resetBtn = msgDiv.querySelector("#btn-chat-reset-pref");

    if (findBtn) {
        findBtn.addEventListener("click", () => {
            findBtn.disabled = true;
            fetchGuidedRecommendations();
        });
    }

    if (editBtn) {
        editBtn.addEventListener("click", () => {
            initializeCineBot(true);
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", () => {
            initializeCineBot(true);
        });
    }

    const container = elements.chatMessages || document.getElementById("chat-messages");
    if (container) {
        container.appendChild(msgDiv);
        container.scrollTop = container.scrollHeight;
    }
}

/**
 * Step 8: Query Recommendation Engine with CineBot Structured Preferences
 */
async function fetchGuidedRecommendations() {
    renderUserMessage("🎬 Find My Movies");

    const typingIndicator = createTypingIndicator();
    elements.chatMessages.appendChild(typingIndicator);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

    try {
        const res = await fetch("/api/chat/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                preferences: cinebotPreferences
            })
        });

        const data = await res.json();
        typingIndicator.remove();

        // Exact Year Rule: If no titles available for specific year, show explicit fallback options
        if (data.not_found_year) {
            renderYearNotFoundMessage(data.year || cinebotPreferences.year);
            return;
        }

        if (data.movies && data.movies.length > 0) {
            renderBotMessage(data.response, data.movies, [
                "🎬 More like these",
                "🔄 New recommendations",
                "🧠 Mind-Bending Sci-Fi",
                "🍿 Feel-Good Comedies"
            ]);
        } else {
            renderBotMessage(
                data.response || "Sorry, no exact titles matched all combined criteria. Try broadening your preferences!",
                [],
                ["Any Genre", "Any Year", "Reset Preferences"]
            );
        }
    } catch (err) {
        typingIndicator.remove();
        console.error("CineBot Recommendation Error:", err);
        renderBotMessage("⚠️ Sorry, I encountered an error searching Netflix recommendations. Please try again!");
    }
}

/**
 * Exact Year Rule: Displays friendly not-found banner with actionable buttons
 */
function renderYearNotFoundMessage(year) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg bot";

    msgDiv.innerHTML = `
        <div class="msg-bubble" style="width: 100%;">
            <div class="chat-fallback-card">
                <p><strong>Sorry, no matching titles are available for ${escapeHtml(String(year))}.</strong></p>
                <p style="color: var(--text-muted); font-size: 0.8rem;">Not available for this year in the catalog.</p>
            </div>
            <div class="chat-action-bar" style="margin-top: 10px;">
                <button class="chat-chip-btn" id="btn-fallback-nearby">Try Nearby Years</button>
                <button class="chat-chip-btn" id="btn-fallback-another">Choose Another Year</button>
                <button class="chat-chip-btn" id="btn-fallback-any">Any Year</button>
            </div>
        </div>
    `;

    const nearbyBtn = msgDiv.querySelector("#btn-fallback-nearby");
    const anotherBtn = msgDiv.querySelector("#btn-fallback-another");
    const anyBtn = msgDiv.querySelector("#btn-fallback-any");

    if (nearbyBtn) {
        nearbyBtn.addEventListener("click", () => {
            cinebotPreferences.year = "Latest Releases";
            fetchGuidedRecommendations();
        });
    }

    if (anotherBtn) {
        anotherBtn.addEventListener("click", () => {
            const promptDiv = document.createElement("div");
            promptDiv.className = "chat-msg bot";
            promptDiv.innerHTML = `<div class="msg-bubble"><strong>Pick another year from below:</strong></div>`;
            elements.chatMessages.appendChild(promptDiv);

            renderBotOptionsMessage("Choose a year:", CINEBOT_YEARS, (newYearItem, yBtn, yGroup) => {
                highlightSelectedChip(yBtn, yGroup);
                cinebotPreferences.year = newYearItem.value;
                renderUserMessage(newYearItem.label);
                showBotTyping(300, () => {
                    renderPreferencesSummary();
                });
            });
        });
    }

    if (anyBtn) {
        anyBtn.addEventListener("click", () => {
            cinebotPreferences.year = "Any Year";
            fetchGuidedRecommendations();
        });
    }

    elements.chatMessages.appendChild(msgDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

/**
 * Helper to render bot message containing single-select chip buttons
 */
function renderBotOptionsMessage(promptHtml, options, onSelectCallback) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg bot";

    const bubbleDiv = document.createElement("div");
    bubbleDiv.className = "msg-bubble";
    bubbleDiv.style.width = "100%";

    const contentDiv = document.createElement("div");
    contentDiv.innerHTML = promptHtml;
    bubbleDiv.appendChild(contentDiv);

    const groupDiv = document.createElement("div");
    groupDiv.className = "chat-options-group";
    groupDiv.style.marginTop = "10px";

    options.forEach(opt => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "chat-chip-btn";
        btn.innerText = opt.label;
        btn.dataset.value = opt.value;

        btn.addEventListener("click", () => {
            // Disable buttons in group to prevent duplicate submissions
            groupDiv.querySelectorAll(".chat-chip-btn").forEach(b => b.disabled = true);
            btn.disabled = false;
            onSelectCallback(opt, btn, groupDiv);
        });

        groupDiv.appendChild(btn);
    });

    bubbleDiv.appendChild(groupDiv);
    msgDiv.appendChild(bubbleDiv);

    elements.chatMessages.appendChild(msgDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

/**
 * Helper to render genre/mood multi-select chips with confirm button
 */
function renderBotMultiSelectGenresMessage(promptHtml, options, onConfirmCallback) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg bot";

    const bubbleDiv = document.createElement("div");
    bubbleDiv.className = "msg-bubble";
    bubbleDiv.style.width = "100%";

    const contentDiv = document.createElement("div");
    contentDiv.innerHTML = promptHtml;
    bubbleDiv.appendChild(contentDiv);

    const groupDiv = document.createElement("div");
    groupDiv.className = "chat-options-group";
    groupDiv.style.marginTop = "10px";

    const selectedGenresSet = new Set();

    options.forEach(opt => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "chat-chip-btn";
        btn.innerText = opt.label;
        btn.dataset.value = opt.value;

        btn.addEventListener("click", () => {
            if (opt.value === "Any") {
                // Instantly advance with Any Genre
                groupDiv.querySelectorAll(".chat-chip-btn").forEach(b => b.disabled = true);
                btn.classList.add("selected");
                onConfirmCallback(["Any Genre"]);
                return;
            }

            // Toggle selection
            if (selectedGenresSet.has(opt.value)) {
                selectedGenresSet.delete(opt.value);
                btn.classList.remove("selected");
            } else {
                selectedGenresSet.add(opt.value);
                btn.classList.add("selected");
            }
        });

        groupDiv.appendChild(btn);
    });

    bubbleDiv.appendChild(groupDiv);

    // Confirm Action Bar
    const actionBar = document.createElement("div");
    actionBar.className = "chat-action-bar";

    const confirmBtn = document.createElement("button");
    confirmBtn.type = "button";
    confirmBtn.className = "chat-btn-confirm";
    confirmBtn.innerHTML = `<span>Continue with Selected</span> <i class="fa-solid fa-arrow-right"></i>`;

    confirmBtn.addEventListener("click", () => {
        groupDiv.querySelectorAll(".chat-chip-btn").forEach(b => b.disabled = true);
        confirmBtn.disabled = true;
        const genresList = Array.from(selectedGenresSet);
        onConfirmCallback(genresList.length > 0 ? genresList : ["Any Genre"]);
    });

    actionBar.appendChild(confirmBtn);
    bubbleDiv.appendChild(actionBar);
    msgDiv.appendChild(bubbleDiv);

    elements.chatMessages.appendChild(msgDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

/**
 * Helper to render optional duration selection chips
 */
function renderBotDurationMessage(promptHtml, options, onSelectCallback) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg bot";

    const bubbleDiv = document.createElement("div");
    bubbleDiv.className = "msg-bubble";
    bubbleDiv.style.width = "100%";

    const contentDiv = document.createElement("div");
    contentDiv.innerHTML = promptHtml;
    bubbleDiv.appendChild(contentDiv);

    const groupDiv = document.createElement("div");
    groupDiv.className = "chat-options-group";
    groupDiv.style.marginTop = "10px";

    options.forEach(opt => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "chat-chip-btn";
        btn.innerText = opt.label;
        btn.dataset.value = opt.value;

        btn.addEventListener("click", () => {
            groupDiv.querySelectorAll(".chat-chip-btn").forEach(b => b.disabled = true);
            btn.disabled = false;
            highlightSelectedChip(btn, groupDiv);
            onSelectCallback(opt);
        });

        groupDiv.appendChild(btn);
    });

    bubbleDiv.appendChild(groupDiv);

    // Skip Button
    const actionBar = document.createElement("div");
    actionBar.className = "chat-action-bar";

    const skipBtn = document.createElement("button");
    skipBtn.type = "button";
    skipBtn.className = "chat-btn-skip";
    skipBtn.innerHTML = `Skip Duration ⏩`;

    skipBtn.addEventListener("click", () => {
        groupDiv.querySelectorAll(".chat-chip-btn").forEach(b => b.disabled = true);
        skipBtn.disabled = true;
        onSelectCallback(null);
    });

    actionBar.appendChild(skipBtn);
    bubbleDiv.appendChild(actionBar);
    msgDiv.appendChild(bubbleDiv);

    elements.chatMessages.appendChild(msgDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function highlightSelectedChip(btn, group) {
    if (group) {
        group.querySelectorAll(".chat-chip-btn").forEach(b => b.classList.remove("selected", "active"));
    }
    if (btn) {
        btn.classList.add("selected");
    }
}

function showBotTyping(delayMs, callback) {
    const indicator = createTypingIndicator();
    elements.chatMessages.appendChild(indicator);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

    setTimeout(() => {
        indicator.remove();
        callback();
    }, delayMs);
}

/**
 * Natural language chat submission handler
 */
async function sendUserMessage(text) {
    renderUserMessage(text);

    // Quick vibe match shortcuts check
    const lower = text.toLowerCase();
    if (lower.includes("marathi") && lower.includes("horror")) {
        cinebotPreferences.language = "Marathi";
        cinebotPreferences.cinema = "Marathi";
        cinebotPreferences.genres = ["Horror"];
        cinebotPreferences.year = "Any Year";
        cinebotPreferences.type = "Movie";
    } else if (lower.includes("hindi") && lower.includes("romance")) {
        cinebotPreferences.language = "Hindi";
        cinebotPreferences.cinema = "Bollywood";
        cinebotPreferences.genres = ["Romance"];
        cinebotPreferences.year = "Any Year";
        cinebotPreferences.type = "Movie";
    } else if (lower.includes("bollywood") && lower.includes("comedy")) {
        cinebotPreferences.language = "Hindi";
        cinebotPreferences.cinema = "Bollywood";
        cinebotPreferences.genres = ["Comedy"];
        cinebotPreferences.year = "Any Year";
        cinebotPreferences.type = "Movie";
    } else if (lower.includes("hollywood") && lower.includes("thriller")) {
        cinebotPreferences.language = "English";
        cinebotPreferences.cinema = "Hollywood";
        cinebotPreferences.genres = ["Thriller"];
        cinebotPreferences.year = "Any Year";
        cinebotPreferences.type = "Movie";
    } else if (lower.includes("sci-fi") || lower.includes("scifi")) {
        cinebotPreferences.genres = ["Sci-Fi"];
    }
    
    // Add typing indicator
    const typingIndicator = createTypingIndicator();
    elements.chatMessages.appendChild(typingIndicator);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: text,
                context: state.chatContext
            })
        });
        const data = await res.json();
        
        typingIndicator.remove();
        state.chatContext = data.updated_context || {};

        if (data.not_found_year) {
            renderYearNotFoundMessage(data.year);
        } else {
            renderBotMessage(data.response, data.movies, data.suggestions);
        }
    } catch (err) {
        typingIndicator.remove();
        renderBotMessage("⚠️ Sorry, I encountered an error searching Netflix recommendations. Please try again!");
        console.error("Chat error:", err);
    }
}

function renderUserMessage(text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg user";
    msgDiv.innerHTML = `<div class="msg-bubble">${escapeHtml(text)}</div>`;
    elements.chatMessages.appendChild(msgDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function renderBotMessage(markdownText, movies = [], suggestions = []) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg bot";
    
    const formattedHtml = formatChatMarkdown(markdownText);
    
    let movieCardsHtml = "";
    if (movies && movies.length > 0) {
        movieCardsHtml = `<div class="chat-movie-list">`;
        movies.forEach(m => {
            const thumb = m.poster || m.poster_url || m.backdrop || m.backdrop_url || "";
            const yr = m.releaseYear || m.release_year || "";
            const genre = (m.genres && m.genres.length > 0) ? m.genres[0] : "";
            const imdb = m.imdb_score || 8.0;
            movieCardsHtml += `
                <div class="chat-movie-card" data-id="${m.id}">
                    <div class="chat-movie-thumb" style="background-image: url('${thumb}');"></div>
                    <div class="chat-movie-info">
                        <div class="chat-movie-title">${escapeHtml(m.title)}</div>
                        <div class="chat-movie-meta">${yr} • ${genre} • ⭐ ${imdb}</div>
                    </div>
                    <span class="chat-movie-score">${m.match_score || 95}%</span>
                </div>
            `;
        });
        movieCardsHtml += `</div>`;
    }

    msgDiv.innerHTML = `
        <div class="msg-bubble" style="width: 100%;">
            <div>${formattedHtml}</div>
            ${movieCardsHtml}
        </div>
    `;

    // Attach click handlers to mini cards
    msgDiv.querySelectorAll(".chat-movie-card").forEach(card => {
        card.addEventListener("click", () => {
            const mId = card.dataset.id;
            openMovieDetail(mId);
        });
    });

    elements.chatMessages.appendChild(msgDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

    if (suggestions && suggestions.length > 0) {
        renderChatSuggestions(suggestions);
    }
}

function renderChatSuggestions(suggestions) {
    if (!elements.chatSuggestions) return;
    elements.chatSuggestions.innerHTML = "";
    if (!suggestions || suggestions.length === 0) return;

    suggestions.forEach(s => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "chat-chip";
        chip.innerText = s;
        chip.addEventListener("click", () => {
            sendUserMessage(s);
        });
        elements.chatSuggestions.appendChild(chip);
    });
}

function createTypingIndicator() {
    const div = document.createElement("div");
    div.className = "chat-msg bot";
    div.innerHTML = `
        <div class="msg-bubble" style="display: flex; gap: 5px; align-items: center; padding: 12px 18px;">
            <span style="animation: pulse 1s infinite;">●</span>
            <span style="animation: pulse 1s infinite 0.2s;">●</span>
            <span style="animation: pulse 1s infinite 0.4s;">●</span>
        </div>
    `;
    return div;
}

function formatChatMarkdown(text) {
    if (!text) return "";
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n• /g, '<br>• ');
}

function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
}

// ==========================================================================
// Toast Utility
// ==========================================================================

let toastTimeout = null;
function showToast(msg) {
    elements.toastMsg.innerText = msg;
    elements.toast.classList.add("show");
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        elements.toast.classList.remove("show");
    }, 3000);
}
