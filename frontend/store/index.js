import Vue from 'vue';
import axios from 'axios';
import Vuex from 'vuex';
import * as types from './mutation-types';
import createPersistedState from 'vuex-persistedstate'
import jwt_decode from 'jwt-decode'
import router from '../router'
Vue.use(Vuex);

const API_URL = process.env.NODE_ENV === "development" ? "http://localhost:8000/api/" : "/api/";
const OBTAIN_URL = API_URL + 'jwt/obtain';
const REFRESH_URL = API_URL + 'jwt/refresh';
const VERIFY_URL = API_URL + 'jwt/verify';
const USERS_URL = API_URL + 'users/';
const CHILDREN_URL = API_URL + 'children/';
const HOLIDAYS_URL = API_URL + 'holidays/';
const REGISTRATIONS_URL = API_URL + 'registrations/';
const CONTENTS_URL = API_URL + 'contents/';
const SECTIONS_URL = API_URL + 'sections/';
const TEAM_MEMBERS_URL = API_URL + 'team_members/';
const MESSAGE_URL = API_URL + 'messages/'
const NEWS_URL = API_URL + 'news/'

const state = {
    accessToken: null,
    currentUser: {},
    users: {},
    children: [],
    holidays: [],
    registrations: [],
    contents: [],
    sections: [],
    team_members: [],
    news: [],
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
    },
    [types.GET_CONTENTS]: (state, payload) => {
        state.contents = payload;
    },
    [types.GET_SECTIONS]: (state, payload) => {
        state.sections = payload;
    },
    [types.GET_TEAM_MEMBERS]: (state, payload) => {
        state.team_members = payload;
    },
    [types.GET_NEWS]: (state, payload) => {
        state.news = payload;
    },
};
const actions = {
    [types.REGISTER]: ({ commit }, payload) => {
        axios.post(
            USERS_URL, payload
        ).then(r => {
            //console.log(r);
        })
    },
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
                //console.log(mutationPayload)
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
            USERS_URL +  id
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
        axios.post(CHILDREN_URL, payload).then((r) => {
            if (r.data) {
                commit(types.CREATE_CHILD, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.UPDATE_CHILD]: ({ commit }, payload) => {
        axios.patch(CHILDREN_URL + payload.id + "/", payload).then((r) => {
            if (r.data) {
                commit(types.UPDATE_CHILD, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.DELETE_CHILD]: ({ commit }, id) => {
        axios.delete(CHILDREN_URL + id).then(() => {
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
        axios.post(REGISTRATIONS_URL, payload).then((r) => {
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
    [types.GET_CONTENTS]: ({ commit }) => {
        axios.get(
            CONTENTS_URL
        ).then((r) => {
            if (r.data) {
                commit(types.GET_CONTENTS, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.GET_SECTIONS]: ({ commit }) => {
        axios.get(
            SECTIONS_URL
        ).then((r) => {
            if (r.data) {
                commit(types.GET_SECTIONS, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.GET_TEAM_MEMBERS]: ({ commit }) => {
        axios.get(
            TEAM_MEMBERS_URL
        ).then((r) => {
            if (r.data) {
                commit(types.GET_TEAM_MEMBERS, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
    [types.CREATE_MESSAGE]: ({ commit }, payload) => {
        axios.post(MESSAGE_URL, payload).catch((e) => {
            console.error(e)
        });
    },
    [types.GET_NEWS]: ({ commit }) => {
        axios.get(
            NEWS_URL
        ).then((r) => {
            if (r.data) {
                commit(types.GET_NEWS, r.data)
            }
        }).catch((e) => {
            console.error(e)
        });
    },
};


// export function base() {
//     return 'http://' + window.location.hostname + ':8000/api'
// }
//
// export function getUser(userID) {
//     return axios.get(base() + '/users/' + userID + '/')
// }

const order_sort = (a, b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0);

const getters = {
    getCurrentUserId: state => state.currentUser.user_id,
    IsAuthenticated: state => state.currentUser.authenticated,
    getUser: state => id => state.users[id] || {},
    getChildren: state => state.children,
    getHolidays: state => state.holidays,
    getRegistrations: state => state.registrations,
    getSections: state => state.sections,
    getContents: state => state.contents,
    getServices: state => state.contents.filter(c => c.section === "service").sort(order_sort),
    getObjectives: state => state.contents.filter(c => c.section === "objectif").sort(order_sort),
    getMethodologies: state => state.contents.filter(c => c.section === "methodologie").sort(order_sort),
    getTeamMembers: state => state.team_members,
    getNews: state => state.news,
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
