import Vue from 'vue';
import axios from 'axios';
import Vuex from 'vuex';
import * as types from './mutation-types';
import createPersistedState from 'vuex-persistedstate'
import jwt_decode from 'jwt-decode'
import router from '../router'
Vue.use(Vuex);

const API_URL = '/api/';
const OBTAIN_URL = API_URL + 'jwt/obtain';
const REFRESH_URL = API_URL + 'jwt/refresh';
const VERIFY_URL = API_URL + 'jwt/verify';
const USERS_URL = API_URL + 'users';
const CHILDREN_URL = API_URL + 'children';
const HOLIDAYS_URL = API_URL + 'holidays';
const REGISTRATIONS_URL = API_URL + 'registrations';

const state = {
    accessToken: null,
    currentUser: {},
    users: {},
    children: [],
    holidays: [],
    registrations: [],
};
const mutations = {
    [types.UPDATE_TOKEN]: (state, payload) => {
        state.accessToken = payload.token;
        state.currentUser = payload.user;
        router.push(payload.redirect)
    },
    [types.LOGOUT]: (state, payload) => {
        state.accessToken = null;
        state.currentUser = {};
        router.push(payload.redirect)
    },
    [types.GET_USER]: (state, payload) => {
        state.users[payload.id] = payload;
    },
    [types.GET_CHILDREN]: (state, payload) => {
        state.children = payload;
    },
    [types.CREATE_CHILD]: (state, payload) => {
        state.children.push(payload);
    },
    [types.UPDATE_CHILD]: (state, payload) => {
        const item = state.children.find(item => item.id === payload.id);
        Object.assign(item, payload);
    },
    [types.DELETE_CHILD]: (state, id) => {
        state.children = state.children.filter(c => c.id !== id)
    },
    [types.GET_HOLIDAYS]: (state, payload) => {
        state.holidays = payload;
    },
    [types.CREATE_REGISTRATION]: (state, payload) => {
        state.registrations.push(payload);
    },
    [types.GET_REGISTRATIONS]: (state, payload) => {
        state.registrations = payload;
    }
};
const actions = {
    [types.UPDATE_TOKEN]: ({ commit }, payload) => {
        axios.post(
            OBTAIN_URL, payload.credentials
        ).then((r) => {
            if (r.data.token) {
                const mutationPayload = {
                    token: r.data.token,
                    user: JSON.parse(atob(r.data.token.split('.')[1])),
                };
                mutationPayload.user.authenticated = true
                mutationPayload.redirect = payload.redirect
                console.log(mutationPayload)
                commit(types.UPDATE_TOKEN, mutationPayload)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.LOGOUT]: ({ commit }) => {
        return commit(types.LOGOUT, { redirect: "/" })
    },
    [types.REFRESH_TOKEN]: ({ state, commit }) => {
        const payload = {
            token: state.accessToken
        };
        return axios.post(
            REFRESH_URL, payload
        ).then((r) => {
            commit(types.UPDATE_TOKEN, r.data.token);
            return r.data.token
        }).catch((e) => {
            console.error(e);
        });
    },
    [types.INSPECT_TOKEN]: ({ dispatch, state }) => {
        return new Promise((resolve, reject) => {
            const token = state.accessToken;
            if (!token) return;
            const decoded = jwt_decode(token);
            const exp = decoded.exp;
            const orig_iat = decoded.orig_iat;
            const now = Date.now() / 1000;
            if ((exp - now) < 1800 && (now - orig_iat) < 628200) {
                dispatch(types.REFRESH_TOKEN).then((token) => resolve(token));
            } else {
                dispatch(types.LOGOUT).then(() => resolve(null));
            }
        });

    },
    [types.GET_USER]: ({ commit }, id) => {
        axios.get(
            USERS_URL + "/" + id
        ).then((r) => {
            if (r.data) {
                commit(types.GET_USER, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.GET_CHILDREN]: ({ commit }) => {
        axios.get(
            CHILDREN_URL
        ).then((r) => {
            if (r.data) {
                commit(types.GET_CHILDREN, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.CREATE_CHILD]: ({ commit }, payload) => {
        axios.post(CHILDREN_URL + "/", payload).then((r) => {
            if (r.data) {
                commit(types.CREATE_CHILD, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.UPDATE_CHILD]: ({ commit }, payload) => {
        axios.patch(CHILDREN_URL + "/" + payload.id + "/", payload).then((r) => {
            if (r.data) {
                commit(types.UPDATE_CHILD, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.DELETE_CHILD]: ({ commit }, id) => {
        axios.delete(CHILDREN_URL + "/" + id).then(() => {
            commit(types.DELETE_CHILD, id);
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.GET_HOLIDAYS]: ({ commit }) => {
        axios.get(
            HOLIDAYS_URL
        ).then((r) => {
            if (r.data) {
                commit(types.GET_HOLIDAYS, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.CREATE_REGISTRATION]: ({ commit, dispatch }, payload) => {
        axios.post(REGISTRATIONS_URL + "/", payload).then((r) => {
            if (r.data) {
                commit(types.CREATE_REGISTRATION, r.data)
            }
        }).catch((e) => {
            console.error(e)
        }).then(() => {
            dispatch(types.GET_CHILDREN);
            dispatch(types.GET_HOLIDAYS);
        });
    },
    [types.GET_REGISTRATIONS]: ({ commit }) => {
        axios.get(
            REGISTRATIONS_URL
        ).then((r) => {
            if (r.data) {
                commit(types.GET_REGISTRATIONS, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },

};


export function base() {
    return 'http://' + window.location.hostname + ':8000/api'
}

export function getUser(userID) {
    return axios.get(base() + '/users/' + userID + '/')
}

const getters = {
    getCurrentUserId: state => state.currentUser.user_id,
    IsAuthenticated: state => state.currentUser.authenticated,
    getUser: state => id => state.users[id],
    getChildren: state => state.children,
    getHolidays: state => state.holidays,
    getRegistrations: state => state.registrations,
}

const store = new Vuex.Store({
    state,
    mutations,
    actions,
    getters,
    plugins: [
        createPersistedState()
    ]
});

export default store;
