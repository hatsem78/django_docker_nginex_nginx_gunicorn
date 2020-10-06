notifications = Vue.component('notifications',{
    props:{
        action: null,
    },
    inject:['$validator'],
    data(){
        return {
            dataSet: [],
            userId: -1,
            countNotification: 0,
            count_is_read: 0,
            count_is_seen: 0,
            urlNotification: ''
        }
    },
    methods:{
        load_data () {
            let self = this;
            HTTP.get(`notification/list`,{
                params: {
                    'action': this.actionList,
                    'user_id': self.userId
                },
            })
            .then((response) => {
                self.dataSet = response.data.data;
                self.count_is_read = response.data[0].count_is_read;
                self.count_is_seen = response.data[0].count_is_seen;
            })
            .catch((err) => {
                store.dispatch({type: 'setLoading',value: false });
                console.log(err);
            });

        },

    },
    created: function() {

    },
    watch:{

    },
    mounted: function() {
        let self = this;
        self.userId = user_id
        self.urlNotification = NOTIFICATION_URL
        self.load_data();
    },
    template: `
        <li class="dropdown"><a class="app-nav__item" href="#" data-toggle="dropdown" aria-label="Show notifications"><i class="fa fa-bell-o fa-lg"></i></a>
          <ul class="app-notification dropdown-menu dropdown-menu-right">
            <li class="app-notification__title">List the notifications.</li>
            <div class="app-notification__content">
              <li>
                  <a class="app-notification__item" href="javascript:;">
                      <span class="app-notification__icon btn-outline-primary" >
                        <span class="fa-stack fa-lg">
                            <i class="fa fa-book"></i>

                        </span>
                      </span>
                      <div>
                        <p class="app-notification__message">You have <span v-text="count_is_read"></span> unread notifications</p>
                      </div>
                </a>
              </li>
              <li>
                <a class="app-notification__item" href="javascript:;">
                    <span class="app-notification__icon btn-outline-primary ">
                        <span class="fa-stack fa-lg">
                            <i class="fa fa-lg fa fa-eye"></i>
                        </span>
                    </span>
                    <div>
                        <p class="app-notification__message">you have <span v-text="count_is_seen"></span> unseen notifications</p>
                    </div>
                </a>
              </li>

              </div>
            </div>
            <li class="app-notification__footer"><a :href="urlNotification">See all notifications.</a></li>
          </ul>
        </li>
    `
});




const app_notification = new Vue({
  el: '#app_notification',
  store,
  components: {
    notifications: notifications,
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
        showDeleteMeetupBeer: false,
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
        show_meetup_beer:function(value){
            let self = this;
            if(value){
                self.showDeleteMeetupBeer = value;
            }
            else{
                self.showDeleteMeetupBeer = value;
                self.tipo = true;
                self.refresh();
            }
        },
        deleteUploadFilesModule: function (id) {
            let self = this;
            store.dispatch({type: 'setLoading',value: true });
            HTTP.delete(`/upload_files_module/${id}/`)
            .then((response) => {

                store.dispatch({type: 'setLoading',value: false });
                self.refresh();
            })
            .catch((err) => {
                notifier.alert('Error ocurrete: ' + err);
                store.dispatch({type: 'setLoading',value: false });
                console.log(err);
            })
        },

        onChangePage: function(page) {
            this.$refs.vuetabeNotitication.changePage(page)
        },
        deleteRow: function(rowData){
            let self = this;
            self.rowDelete = rowData.id;
            self.show_meetup_beer(true);
        },
        editRow: function (value) {
            let self = this;
            
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

	},
})

