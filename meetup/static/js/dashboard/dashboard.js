//WTrjW5aPKYW8wATg_6m4BQ
Vue.component('date-picker', VueBootstrapDatetimePicker);
Vue.component("v-select", VueSelect.VueSelect);

$("#dashboard").removeClass('active');
$("#create_meetup_beer").addClass('active');

dashboard = Vue.component('dashboard',{
    props:{
        action: null,
    },
    inject:['$validator'],
    data(){
        return {
            dataSet: [],
            userId: -1,
            actionList: Boolean(this.action)
        }
    },
    methods:{
        load_data () {
            let self = this;
            HTTP.get(`meetup/list`,{
                params: {
                    'action': this.actionList,
                    'user_id': self.userId
                },
            })
            .then((response) => {
                self.dataSet = response.data;
            })
            .catch((err) => {
                store.dispatch({type: 'setLoading',value: false });
                console.log(err);
            });

        },
        registration (id) {
            console.log(id)
        /*{
            'user': self.user.pk,
            'meetup': meetup.pk,
            'user_check_in': True
        }*/
        let self = this;
        return HTTP.post('registration_check_in_user/registration/', {
            'user': self.userId,
            'meetup': id,
            'user_check_in': false
        })
            .then((response) => {
                notifier.info('Has been successfully registered');
                return true
            })
            .catch((err) => {
                console.log(err)
                notifier.warning('You are already registered for the event');
                return false
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
        self.load_data();
    },
    template: `

        <div class="row">
            <div  v-if="dataSet.length > 0" class="col-md-6" v-for="(info, id) in dataSet" :key="id">
              <div class="tile">
                <h3 class="tile-title">{{ info.name }}</h3>
                <div class="tile-body">{{ info.description}}</div>
                <div class="tile-body">Direction: {{ info.direction}}</div>
                <div class="tile-body">Datetime Event: {{ info.date}}</div>
                <div class="tile-footer"><a class="btn btn-primary" href="#" @click="registration(info.id)">Register for the event</a></div>
              </div>
            </div>

            <div v-else="">
                Does not have a meetup list to check in
            </div>

        </div>
    `
});

check_in = Vue.component('check_in',{
    props:{
        action: null,
    },
    inject:['$validator'],
    data(){
        return {
            dataSet: [],
            userId: -1,
            actionList: Boolean(this.action)
        }
    },
    methods:{
        load_data () {
            let self = this;
            HTTP.get(`meetup_enroll_invite_users/list`,{
                params: {
                    'action': this.actionList,
                    'user_id': self.userId
                },
            })
            .then((response) => {
                self.dataSet = response.data;
            })
            .catch((err) => {
                store.dispatch({type: 'setLoading',value: false });
                console.log(err);
            });

        },
        check_in (id) {
            let self = this;

            return HTTP.put('registration_check_in_user/check_in/' + id, {
                'user': self.userId,
                'meetup': id,
                'user_check_in': true
            })
            .then((response) => {
                if(Object.keys(response.data).length > 0 && Object.keys(response.data).indexOf('msg-error') < 0){
                    self.load_data();
                    notifier.info('You have successfully registered')
                    return true;
                } else {
                    notifier.warning('You cannot register')
                }
            })
            .catch((err) => {
                console.log(err)
                notifier.error('You are already registered for the event');
                return false
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
        self.load_data();
        console.log('check_in')
    },
    template: `

        <div>
            <div  v-if="dataSet.length > 0" class=" row col-md-6" v-for="(info, id) in dataSet" :key="id">
              <div class="tile">
                <h3 class="tile-title">{{ info.meetup_name }}</h3>
                <div class="tile-body">{{ info.meetup_description}}</div>
                <div class="tile-body">Direction: {{ info.meetup_direction}}</div>
                <div class="tile-body">Datetime Event: {{ info.meetup_date}}</div>
                <div class="tile-footer"><a class="btn btn-primary" href="#" @click="check_in(info.id)">Check in</a></div>
              </div>
            </div>
            <div v-if="dataSet.length <= 0">
                It does not have a list of beer meetings
            </div>

        </div>
    `
});


const app_dashboard = new Vue({
  el: '#app_dashboard',
  store,
  components: {
    dashboard: dashboard,
    check_in: check_in
  },
})

