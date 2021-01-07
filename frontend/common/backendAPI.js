import * as types from '../store/mutation-types'
import axios from 'axios'
import store from '../store'
import router from '../router'

axios.interceptors.request.use(
    config => {
        if (store.state.accessToken) {
            config.headers.Authorization = `JWT ${store.state.accessToken}`
        }
        return config
    },
    err => {
        return Promise.reject(err)
    })

axios.interceptors.response.use(
    response => {
        return response
    },
    error => {
        console.log('[Response error!]', error.response)
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // Using logout instead of login for renew state
                    store.dispatch(
                        types.REFRESH_TOKEN
                    ).then((token) => {
                        if (!token) {
                            store.commit(types.LOGOUT, {
                                router: router,
                                redirect: 'login'
                            })
                            return;
                        }
                        const config = error.config;
                        config.headers = { Authorization: `JWT ${token}` }
                        return new Promise((resolve, reject) => {
                            axios.request(config).then(response => {
                                resolve(response);
                            }).catch((error) => {
                                reject(error)
                            })
                        });
                    })
                    break
                case 500:
                    console.log(error.response.statusText)
                    break
            }
        }
        return Promise.reject(error.response.data)
    })
