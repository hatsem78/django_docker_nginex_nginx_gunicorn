create_meetup_beer = Vue.component('create_meetup_beer',{
    props:{
        action: null,
    },
    inject:['$validator'],
    data(){
        return {
            tableWeather: [],
            city: null,
            formAdd: false,
            datos:{
                id:'',
                name: '',
                date:'',
                description: '',
                maximum_temperature:'',
                direction: '',
                hour: '',
            },
            titulo: "Create Meetup Beer"
        }
    },
    methods:{
        loadDataWeather(){
            let self = this;
            store.dispatch({type: 'setLoading',value: true });
            HTTP.get(`check_weather/list`,{
                params: {
                    'city': self.city,
                },
            })
            .then((response) => {
                if(Object.values(response.data).indexOf('404') >= 0){
                     self.tableWeather = [];
                    notifier.warning(response.data['message'])
                } else {
                    self.tableWeather = response.data;
                }
                store.dispatch({type: 'setLoading',value: false });
            })
            .catch((err) => {
                store.dispatch({type: 'setLoading',value: false });
                console.log(err);
            });

        },
        doFilter(){
            this.loadDataWeather();
        },
        resetFilter(){
            this.city = '';
            this.loadDataWeather();
        },
        cancelar(){
            eventBus.$emit('cancelCreateMeetup')
        },
        cancelarForm(){
            this.formAdd = false;
        },
        saveForm(){
            let self = this;

            self.datos['date'] = `${self.datos.date} ${self.datos.hour}:00`;


            store.dispatch({type: 'setLoading',value: true});
            HTTP.post(`meetup/create/`,self.datos)
            .then(async (response) => {
                if(Object.keys(response.data).length > 0 && Object.keys(response.data).indexOf('msg-error') < 0){
                    this.formAdd = false;
                    notifier.info('The meetup was successfully saved')
                } else {
                    notifier.warning('The meetup could not be saved')
                }
                store.dispatch({type: 'setLoading',value: false});
            })
            .catch((err) => {
                store.dispatch({type: 'setLoading',value: false});
                console.log(err);
            });


        },
        addMeetupe(value){
           this.formAdd = true;
           this.datos.date = value.date;
           this.datos.maximum_temperature  = value.temp;
        }
    },
    created: function() {

    },
    watch:{

    },
    mounted: function() {
        let self = this;
        self.loadDataWeather();
    },
    template: `

        <div>
            <!-- List of the weather -->
            <div class="col-md-8" v-if="!formAdd">
              <div class="tile">
                <div class="tile-title-w-btn">
                  <h3 class="title">Weather list for 16 days</h3>
                  <div class="form-inline form-group mb-3">
                        <input v-model="city" class="form-control" @keyup.enter="doFilter"
                        placeholder="City,code ">
                        <button class="btn btn-primary" @click="doFilter">Go</button>
                        <button class="btn btn-default" @click="resetFilter">Reset</button>
                        <button class="btn btn-secondary m-progress" @click="cancelar()">Cancel</button>
                  </div>
                </div>
                <div class="tile-body">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>#</th>
                          <th>Day Date</th>
                          <th>temperature</th>
                          <th>weather description</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-if="tableWeather.length > 0" v-for="(info, id) in tableWeather" :key="id">
                          <td>
                            <a class="btn-outline-danger  btn-danger"
                                 @click="addMeetupe(info)"
                                href="#" data-toggle="tooltip" title="Add"
                                >
                               <i class="fa fa-plus-circle btn-outline-primary"></i>
                            </a>
                          </td>
                          <td>{{ info.date_day }}</td>
                          <td>{{ info.temp }}</td>
                          <td>{{ info.weather_description }}</td>
                        </tr>
                        <tr v-else="" >
                            <td></td>
                            <td>City not found</td>
                            <td></td>
                            <td></td>
                        </tr>

                      </tbody>
                    </table>
                </div>
              </div>
            </div>


            <!--add form -->
            <div class="card col-md-10" v-else="">
                <div class="card-header"><h4 class="card-title">  {{ titulo }}</h4></div>
                <div class="card-body">
                
                    <div class="row">
                    <div class="col-md-6 ">
                        <div class="form-group">
                            <label>Name Meetup Beer*</label>
                            <div  :class="[
                                      { 
                                        'has-error': errors.first('name'), 
                                        'has-success': !errors.first('name') && datos.name !== ''
                                      }, 
                                      ]">
                                      
                                <input 
                                    type="text" 
                                    name="name" id="name" 
                                    placeholder="name"  
                                    v-model='datos.name'
                                    v-validate="'required:true|max:127|alphanumeric'" 
                                    :class="{
                                        'input': true, 
                                        'has-error': errors.first('name') && datos.name == '', 
                                        'form-control': true
                                    }"
                                >
                                <div class="errors help-block">
                                    <span v-show="errors.first('name')"
                                        class="help error">{{ errors.first('name') }}
                                    </span>
                                </div> 
                            </div>  
                        </div>
                    </div>
                </div>

                    <div class="row">
                        <div class="col-md-6 ">
                            <div class="form-group">
                                <label>Date*</label>
                                <div  :class="[
                                          {
                                            'has-error': errors.first('date'),
                                            'has-success': !errors.first('date') && datos.date !== ''
                                          },
                                          ]">

                                    <input
                                        type="text"
                                        :disabled="true"
                                        name="date" id="date"
                                        placeholder="Date"
                                        v-model='datos.date'
                                        :class="{
                                            'input': true,
                                            'form-control': true
                                        }"
                                    >
                                    <div class="errors help-block">
                                        <span v-show="errors.first('date')"
                                            class="help error">{{ errors.first('date') }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-2">
                            <div class="form-group">
                                <label>Hour</label>
                                <div  :class="[
                                          {
                                            'has-error': errors.first(''),
                                            'has-success': !errors.first('hour') && datos.hour !== ''
                                          },
                                          ]">

                                    <input
                                        type="text"
                                        name="hour"
                                        id="hour"
                                        placeholder=""
                                        v-model='datos.hour'
                                        v-validate="'required: true|hours_value'"
                                        :class="{
                                            'input': true,
                                            'has-error': errors.first('hour') && datos.hour == '',
                                            'form-control': true
                                        }"
                                    >
                                    <div class="errors help-block">
                                        <span v-show="errors.first('hour')"
                                            class="help error">{{ errors.first('hour') }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group">
                                <label>Description</label>
                                <div id="comment-add" :class="{ 'custom-actions': true, ' has-error': errors.first('description'),
                                    'has-success': !errors.first('description') && datos.description !== '' }">
                                <textarea
                                    name="description"
                                    id="description"
                                    rows="5"
                                    maxlength="197"
                                    placeholder="Description"
                                    v-model='datos.description'
                                    v-validate="'maxCustom:198|remarks'"
                                    :class="{'input': true, 'has-error': errors.first('description'), 'form-control': true }"
                                >
                                </textarea>

                                <div class="errors help-block" id="description-error">
                                    <span v-show="errors.first('description')"
                                        class="help error">{{ errors.first('description') }}
                                    </span>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-6 pr-1">
                            <div class="form-group">
                                <label>Temperature</label>
                                <div  :class="[
                                          {
                                            'has-error': errors.first('maximum_temperature'),
                                            'has-success': !errors.first('maximum_temperature') && datos.maximum_temperature !== ''
                                          },
                                          ]">

                                    <input
                                        :disabled="true"
                                        type="text"
                                        name="maximum_temperature"
                                        id="maximum_temperature"
                                        placeholder="Temperature"
                                        v-model='datos.maximum_temperature'
                                        :class="{
                                            'input': true,
                                            'form-control': true
                                        }"
                                    >
                                    <div class="errors help-block">
                                        <span v-show="errors.first('maximum_temperature')"
                                            class="help error">{{ errors.first('maximum_temperature') }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group">
                                <label>Direction</label>
                                <div  :class="[
                                          {
                                            'has-error': errors.first('direction'),
                                            'has-success': !errors.first('direction') && datos.direction !== ''
                                          },
                                          ]">

                                    <input
                                        type="text"
                                        name="direction"
                                        id="direction"
                                        placeholder="Direction"
                                        v-model='datos.direction'
                                        v-validate="'maxCustom:100|alphanumeric'"
                                        :class="{
                                            'input': true,
                                            'has-error': errors.first('direction') && datos.direction == '',
                                            'form-control': true
                                        }"
                                    >
                                    <div class="errors help-block">
                                        <span v-show="errors.first('direction')"
                                            class="help error">{{ errors.first('direction') }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>



                    <div class="row">
                        <div class="col-md-12 text-right">
                            <button
                                type="button"
                                class="btn btn-secondary m-progress"
                                @click="cancelarForm()"
                            >
                                Cancelar
                            </button>
                            <button
                                type="submit"
                                class="btn btn-primary"
                                @click="saveForm()"
                            >
                                Save
                            </button>
                        </div>
                    </div>
                </div>
            </div>





        </div>
    `
});