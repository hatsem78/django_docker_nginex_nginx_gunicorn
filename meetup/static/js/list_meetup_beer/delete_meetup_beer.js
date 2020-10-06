//WTrjW5aPKYW8wATg_6m4BQ
Vue.component('date-picker', VueBootstrapDatetimePicker);
Vue.component("v-select", VueSelect.VueSelect);

let delete_meetup_beer = Vue.component('delete_meetup_beer',{
    props:{
        show_delete_log: true,
        row_delete: null
    },
    inject:['$validator'],
    data(){
        return {
            showDeleteLog: this.show_delete_log,
            correctDelete: false,
            titleDelete: 'Are you sure?',
            infoDelete: 'You will not be able to recover this Meetup Beer!',
            rowDelete: this.row_delete

        }
    },
    methods:{
        cancelDelete(){
             this.$emit('cancelCreateMeetup', false)
        },
        deleteLog(){
            let self = this;
            store.dispatch({type: 'setLoading',value: true });
            HTTP.delete(`meetup/delete/${self.rowDelete}`)
            .then((response) => {
                self.correctDelete = true;
                self.titleDelete = 'Deleted!'
                self.infoDelete = 'Your Meetup Beer  has been deleted.';
                store.dispatch({type: 'setLoading',value: false });
                eventBus.$emit('deleteMeetupBeer')
            })
            .catch((err) => {
                eventBus.$emit('deleteMeetupBeer')
                store.dispatch({type: 'setLoading',value: false });
                notifier.alert('Error ocurrete: ' + err);
                console.log(err);
            });

        }

    },
    created: function() {

    },
    watch:{

    },
    mounted: function() {
        let self = this;

    },
    template: `

        <div class="sweet-alert showSweetAlert visible" data-custom-class=""
            data-has-cancel-button="true" data-has-confirm-button="true" data-allow-outside-click="false"
            data-has-done-function="true" data-animation="pop" data-timer="null" style="display: block; margin-top: -157px;">
            <div class="sa-icon sa-error" style="display: none;">
              <span class="sa-x-mark">
                <span class="sa-line sa-left"></span>
                <span class="sa-line sa-right"></span>
              </span>
            </div>
            <div class="sa-icon sa-warning pulseWarning" :style="[{'display': correctDelete ? 'none' : 'block'}]">
              <span class="sa-body pulseWarningIns"></span>
              <span class="sa-dot pulseWarningIns"></span>
            </div>
            <div class="sa-icon sa-info" style="display: none;"></div>

            <div class="sa-icon sa-success" :style="[{'display': correctDelete ? 'block' : 'none'}] ">
                <span class="sa-line sa-tip"></span>
                <span class="sa-line sa-long"></span>

              <div class="sa-placeholder"></div>
              <div class="sa-fix"></div>
            </div>

            <div class="sa-icon sa-custom" style="display: none;"></div>
                <h2>{{ titleDelete }}</h2>
                <p style="display: block;">
                    {{ infoDelete }}
                </p>

                <fieldset>
                  <input type="text" tabindex="3" placeholder="">
                  <div class="sa-input-error"></div>
                </fieldset>

                <div class="sa-error-container">
                <div class="icon">!</div>
                <p>Not valid!</p>

            </div>
            <div class="sa-button-container">
                <button class="cancel" tabindex="2" @click="cancelDelete" style="display: inline-block; box-shadow: none;" v-if="!correctDelete">
                    Cancel Delete
                </button>
                <div class="sa-confirm-button-container" v-if="!correctDelete">
                    <button class="confirm" tabindex="1"
                        @click="deleteLog"
                        style="display: inline-block; background-color: rgb(140, 212, 245); box-shadow: rgba(140, 212, 245, 0.8) 0px 0px 2px, rgba(0, 0, 0, 0.05) 0px 0px 0px 1px inset;">
                        Yes, delete it!
                    </button>
                </div>

                <div class="sa-confirm-button-container" @click="cancelDelete" v-else="">
                    <button class="confirm" tabindex="1" s
                        tyle="display: inline-block; background-color: rgb(140, 212, 245); box-shadow: rgba(140, 212, 245, 0.8) 0px 0px 2px, rgba(0, 0, 0, 0.05) 0px 0px 0px 1px inset;">
                        OK
                    </button>
                </div>
            </div>
        </div>
    `
});
