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
const FORGET_PASSWORD_URL = API_URL + 'reset-password/'

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
    capacity_loading: false,
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
    [types.SET_CAPACITY_LOADING]: (state, payload) => {
        state.capacity_loading = payload;
    },
    [types.GET_HOLIDAYS_SECTION_CAPACITY]: (state, payload) => {
        const holidays = [];
        for (const holiday of state.holidays) {
            if (holiday.id !== payload.holiday) {
                holidays.push(holiday)
                continue;
            }
            const sections = [];
            for (const section of holiday.sections) {
                section.capacities = payload.capacities[section.section_id]
                sections.push(section);
            }
            holiday.sections = sections;
            holidays.push(holiday);
        }
        state.holidays = holidays;
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
        return new Promise((resolve) => {
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
                resolve({success: true});
            }).catch((e) => {
                resolve({success: false, error: e});
            });
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
    [types.GET_HOLIDAYS_SECTION_CAPACITY]: ({ commit }, payload) => {
        commit(types.SET_CAPACITY_LOADING, true);
        axios.get(
            `${HOLIDAYS_URL}${payload.holiday_id}/get_capacity`
        ).then((r) => {
            if (r.data) {
                commit(types.GET_HOLIDAYS_SECTION_CAPACITY, {
                    holiday: payload.holiday_id,
                    capacities: r.data
                });
                commit(types.SET_CAPACITY_LOADING, false);
            }
        }).catch((e) => {
            console.error(e)
        })
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
    [types.FORGOT_PASSWORD]: ({}, payload) => {
        axios.post(FORGET_PASSWORD_URL, payload).catch((e) => {
            console.error(e)
        });
    },
    [types.VERIFY_FORGOT_PASSWORD_TOKEN]: ({}, payload) => {
        return new Promise((resolve) => {
            axios.get(FORGET_PASSWORD_URL + "token-validation?token=" + payload.token)
                .then((r) => {
                    resolve({success: r.status === 200})
                })
                .catch((e) => {
                    resolve({success: false}
                )
            })
        });
    },
    [types.RESET_PASSWORD]: ({}, payload) => {
        return new Promise((resolve) => {
            axios.post(FORGET_PASSWORD_URL + "submit/?token=" + payload.token, {password: payload.password})
                .then((r) => {
                    resolve({success: true})
                })
                .catch((e) => {
                    resolve({success: false, error: e})
                });
        })
    },
    [types.GET_CHILD_SECTION]: ({}, payload) => {
        return new promise((resolve) => {
            axios.get(HOLIDAYS_URL + payload.holiday_id + "/get_section_for_child?child_id=" + payload.child_id)
                .then((r) => {
                    resolve(Object.assign(r.data, {success: true}));
                })
                .catch((e) => {
                    resolve({success: false, error: e})
                });
        })
    },
};

export const getChildSection = (payload) =>
    new Promise((resolve) => {
            axios.get(HOLIDAYS_URL + payload.holiday_id + "/get_section_for_child?child_id=" + payload.child_id)
                .then((r) => {
                    resolve(Object.assign(r.data, {success: true}));
                })
                .catch((e) => {
                    resolve({success: false, error: e})
                });
        })


const getters = {
    getCurrentUserId: state => state.currentUser.user_id,
    IsAuthenticated: state => state.currentUser.authenticated,
    getUser: state => id => state.users[id] || {},
    getChildren: state => state.children,
    getHolidays: state => state.holidays,
    getRegistrations: state => state.registrations,
    getSections: state => state.sections,
    getContents: state => state.contents,
    getNews: state => state.news,
    getTeamMembers: state => state.team_members,
    getCapacityLoading: state => state.capacity_loading,
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
