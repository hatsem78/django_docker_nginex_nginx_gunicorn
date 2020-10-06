/**
 * Created by octavio on 19/12/17.
 */


const store = new Vuex.Store({
    state: {
        loading: false,
        title_session: '',
        description_page: '',
        tittle_right: '',
        advertiser: '',

    },
    getters: {
        getLoading: state => state.loading,
        getTitleSession: state => state.title_session,
        getDescriptionPage: state => state.description_page,
        getTittleRight: state => state.tittle_right,
        getAdvertiserSelect: state => state.advertiser,
    },
    mutations: {
        setAdvertiserSelect(state, payload) {
            eval('state.advertiser = payload.value');
        },
        setLoading(state, payload) {
            eval('state.loading = payload.value');
        },
        setTitleSession(state, payload) {
            eval('state.title_session = payload.value');
        },
        setDescriptionPage(state, payload) {
            eval('state.description_page = payload.value');
        },
        setTittleRight(state, payload) {
            eval('state.tittle_right = payload.value');
        },
    },
    actions: {
        setAdvertiserSelect({ commit }, payload) {
            commit('setAdvertiserSelect', payload);
        },
        setLoading({ commit }, payload) {
            commit('setLoading', payload);
        },
        setTitleSession({ commit }, payload) {
            commit('setTitleSession', payload);
        },
        setDescriptionPage({ commit }, payload) {
            commit('setDescriptionPage', payload);
        },
        setTittleRight({ commit }, payload) {
            commit('setTittleRight', payload);
        },
        /*getactionApi({ commit }, payload) {
            HTTP.get('/user/', {
                params: {
                    's': session_id
                }
            }).then(function (response) {
                commit({
                    type: '',
                    value: valor
                });
            });
        }*/
    },
});
