// state.js - Central Application State
export const App = {
    user: null,
    token: null,
    activeConversationId: null,
    conversations: {},
    isGenerating: false,
    arenaMode: false,
    tallyPrompt: 0,
    tallyComp: 0,
    modelsCache: null,
    activeModelId: null
};

export function saveSession(user, token) {
    App.user = user;
    App.token = token;
    sessionStorage.setItem('synora_user', JSON.stringify(user));
    sessionStorage.setItem('synora_token', token);
}

export function loadSession() {
    const savedUser = sessionStorage.getItem('synora_user');
    const savedToken = sessionStorage.getItem('synora_token');
    if (savedUser && savedToken) {
        try {
            App.user = JSON.parse(savedUser);
            App.token = savedToken;
            return true;
        } catch (e) {
            clearSession();
        }
    }
    return false;
}

export function clearSession() {
    sessionStorage.removeItem('synora_user');
    sessionStorage.removeItem('synora_token');
    App.user = null;
    App.token = null;
}
