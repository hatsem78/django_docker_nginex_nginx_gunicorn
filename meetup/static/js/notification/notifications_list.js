Vue.component('date-picker', VueBootstrapDatetimePicker);
Vue.component("v-select", VueSelect.VueSelect);
Vue.component('vuetable', window.Vuetable.Vuetable);

Vue.component('vuetable-pagination', window.Vuetable.VuetablePagination);
Vue.component('vuetable-pagination-info', window.Vuetable.VuetablePaginationInfo);
const app_notification_list = new Vue({
  el: '#app_notification_list',
  store,
  components: {
    delete_notification: delete_notification,
  },
  data: {
        search_term: '',
        moreParams: {},
        filterText: '',
        fieldes: [
            {
                name: 'id',
                title: 'id',
                fieldIndex: 1,
                sortField: 'id',

            },
            {
                name: 'user_name',
                title: 'User Name',
                sortField: 'user_name'
            },
            {
                name: 'text',
                title: 'Notification',
                sortField: 'text'
            },
            {
                name: 'is_seen',
                title: 'Is Seen',
                sortField: 'is_seen'
            },
            {
                name: 'is_read',
                title: 'Is Read',
                sortField: 'is_read'
            },
            {
              name: '__slot:is_seen',   // <----
              title: 'Is Seen',
              titleClass: 'justify aligned',
              dataClass: 'justify aligned'
            },

            {
              name: '__slot:actions',   // <----
              title: 'Actions',
              titleClass: 'center aligned',
              dataClass: 'center aligned'
            }
        ],
        sortOrder: [
            { field: 'id', direction: 'desc' }
        ],
        css: {
            table: {
                tableClass: 'table table-responsive table-striped table-bordered table-hovered',
                loadingClass: 'loading',
                ascendingIcon: 'fa fa-chevron-up',
                descendingIcon: 'fa fa-chevron-down',
                handleIcon: 'fa-align-justify',
            },
            pagination: {
                infoClass: 'pull-left',
                wrapperClass: 'vuetable-pagination pull-right',
                activeClass: 'btn-primary',
                disabledClass: 'disabled',
                pageClass: 'btn btn-border',
                linkClass: 'btn btn-border',
                icons: {
                  first: 'fa fa-chevron-left',
                  prev: 'fa fa-chevron-left',
                  next: 'fa fa-chevron-right',
                  last: 'fa fa-chevron-right',
                }
            }
        },
        showDeleteNotification: false,
        showNotification: false,
        rowDelete: -1,
        dataset: [],
    },
    mounted: function() {

    },
    methods: {
        onPaginationData: function(paginationData) {
            this.$refs.paginationNotification.setPaginationData(paginationData)
        },
        show_notifiation:function(value){
            let self = this;
            if(value){
                self.showDeleteNotification = value;
            }
            else{
                self.showDeleteNotification = value;
                self.tipo = true;
                self.refresh();
            }
        },
        onChangePage: function(page) {
            this.$refs.vuetabeNotitication.changePage(page)
        },
        deleteRow: function(rowData){
            let self = this;
            self.rowDelete = rowData.id;
            self.show_notifiation(true);
        },
        isSeenRow: function (rowData) {
            let self = this;

            return HTTP.put('notification/is_seen/' + rowData.id, {
                'is_seen': true
            })
            .then((response) => {
                if(Object.keys(response.data).length > 0 && Object.keys(response.data).indexOf('msg-error') < 0){
                    self.load_data();
                    notifier.info('Save successfully')
                    self.refresh();
                    return true;
                } else {
                    notifier.warning('You cannot save')
                }
            })
            .catch((err) => {
                console.log(err)
                notifier.error('You cannot save');
                return false
            });
            
        },
        onLoading: function() {

        },
        doFilter () {
            this.moreParams = {
                'filter': this.filterText
            }
            Vue.nextTick( () => this.$refs.vuetabeNotitication.refresh())
        },
        resetFilter () {
            let self = this;
            this.filterText = "";
            this.moreParams = {}
            self.$nextTick(()=>{
              self.$refs.vuetabeNotitication.refresh();
              store.dispatch({type: 'setLoading',value: false });
            })
        },
        refresh: function() {
            let self = this;
            self.$nextTick(()=>{
              self.$refs.vuetabeNotitication.refresh();
              store.dispatch({type: 'setLoading',value: false });
            })
        },
        onLoaded:function () {

        },

        load_data () {
            let self = this;
            HTTP.get(`notification/list_page`,{
                params: {
                    'filter': this.filterText,
                },
            })
            .then((response) => {
                /*for(seleccion in response.data){
                    self.advertiser.push({'id': response.data[seleccion]['id'], 'name': response.data[seleccion]['name'] });
                }*/

                self.dataset = response.data.data;

            })
            .catch((err) => {
                store.dispatch({type: 'setLoading',value: false });
                console.log(err);
            });


        },
    },
    watch: {
        

    },
    created() {
	    let self = this;
        eventBus.$on('cancelNotification', (payload) => {
          self.showNotification = false;
        });

        eventBus.$on('deleteNotification', (payload) => {
            self.showDeleteNotification = false;
            self.refresh();
        });
	},
})

