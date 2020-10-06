//WTrjW5aPKYW8wATg_6m4BQ
Vue.component('date-picker', VueBootstrapDatetimePicker);
Vue.component("v-select", VueSelect.VueSelect);
Vue.component('vuetable', window.Vuetable.Vuetable);

Vue.component('vuetable-pagination', window.Vuetable.VuetablePagination);
Vue.component('vuetable-pagination-info', window.Vuetable.VuetablePaginationInfo);

$("#dashboard").removeClass('active');
$("#check_in").addClass('active');

const app_dashboard = new Vue({
  el: '#app_create_meeetup_beer',
  store,
  components: {
    create_meetup_beer: create_meetup_beer,
    delete_meetup_beer: delete_meetup_beer
  },
  data: {
        titulo:'Add Upload Meetup',
        tipo: true,
        loading: false,
        message: null,
        id_update: 0,
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
                name: 'date',
                title: 'Date Meetup',
                sortField: 'date'
            },
            {
                name: 'description',
                title: 'Description',
                sortField: 'description'
            },
            {
                name: 'count_beer',
                title: 'Count beer event',
                sortField: 'count_beer'
            },
            {
                name: 'count_box_beer',
                title: 'Count Box Beer',
                sortField: 'count_box_beer'
            },
            {
                name: 'maximum_temperature',
                title: 'Temperature for day',
                sortField: 'maximum_temperature'
            },
            {
                name: 'count_participants',
                title: 'Count Participants',
                sortField: 'count_participants'
            },
            {
                name: 'direction',
                title: 'Direction',
                sortField: 'direction'
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
        action: true,
        showDeleteMeetupBeer: false,
        showMeeetupBeer: false,
        rowDelete: -1,
        dataset: [],
    },
    mounted: function() {

    },
    methods: {
        onPaginationData: function(paginationData) {
            this.$refs.paginationCreateMeeupBeer.setPaginationData(paginationData)
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
            this.$refs.vuetabeCreateMeeupBeer.changePage(page)
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
            Vue.nextTick( () => this.$refs.vuetabeCreateMeeupBeer.refresh())
        },
        resetFilter () {
            let self = this;
            this.filterText = "";
            this.moreParams = {}
            self.$nextTick(()=>{
              self.$refs.vuetabeCreateMeeupBeer.refresh();
              store.dispatch({type: 'setLoading',value: false });
            })
        },
        refresh: function() {
            let self = this;
            self.$nextTick(()=>{
              self.$refs.vuetabeCreateMeeupBeer.refresh();
              store.dispatch({type: 'setLoading',value: false });
            })
        },
        onLoaded:function () {

        },

        load_data () {
            let self = this;
            HTTP.get(`import_file_log_list`,{
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
        addMeetupBeer: function () {
            let self = this;
            self.titulo = "Add Meetup Beer";
            self.showMeeetupBeer = true;

        },

    },
    watch: {
        

    },
    created() {
	    let self = this;

		eventBus.$on('cancelCreateMeetup', (payload) => {
          self.showMeeetupBeer = false;
        });

        eventBus.$on('deleteMeetupBeer', (payload) => {
            self.deleteMeetupBeer = false;
            self.refresh();
        });

    },
})

