var csrftoken = $("#tocken").val();
Vue.use(VeeValidate);
Vue.use(VTooltip)
const eventBus = new Vue();

const HTTP = axios.create({
    baseURL: '/' + API_PREFIX,
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        'X-CSRFToken': CRFTOKEN,
    }
});

const company = "Meetup Beer"

const urlStatic = URL_STATIC;

const typeUser = TYPE_USER;
const user_id = USER_ID

const today = moment({ hour: '00', minute: '00' });

axios.defaults.headers.common['X-CSRFToken'] = CRFTOKEN;


Vue.filter('truncate', function (text, stop, clamp) {
    return text.slice(0, stop) + (stop < text.length ? clamp || '...' : '')
});

const padStart = function (replace, char, value) {
    let result = '';
    for (var x = value.length; x < replace; x++) {
        result += char;
    }

    return result + value;
};


Vue.use(VeeValidate, {
    inject: false,
    locale: 'es'
});

function formatNumber(number) {
    return (number).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    console.log('juan')
}

VeeValidate.Validator.extend('alpha', {
    getMessage: field => {
        return ('Se ingresaron caracteres invalidos')
    },
    validate: value => /^[a-zA-Z]+$/.test(value)
});


VeeValidate.Validator.extend('alpha_lastname', {
    getMessage: field => {
        return ('Se ingresaron caracteres invalidos')
    },
    validate: value => /^[a-zA-Z\/\ ]+$/.test(value)
});

VeeValidate.Validator.extend('duplicate_passenger', {
    getMessage: field => {
        return ('No pueden existir dos pasajeros con el mismo nombre y segundo nombre en la reserva!')
    },
    validate(value, obj) {
        let input = obj[0];
        let inputFirstName = $("#" + "firstname" + input.key[0]).val();
        if (input.control[0] !== undefined && input.control[0].indexOf((value + inputFirstName).toUpperCase()) > -1) {
            return false;
        }
        else {
            return true;
        }
    }
});


VeeValidate.Validator.extend('alphanumeric', {
    getMessage: field => {
        return ('Se ingresaron caracteres invalidos')
    },
    validate: value => /^[A-Za-z0-9/ñ/Ñ/\ ]+$/.test(value)
});


VeeValidate.Validator.extend('decimal', {
    getMessage: field => {
        return ('Invalid number only two decimal places')
    },
    validate: value => /^\d+(\.\d{1,2})?$/.test(value)
});

VeeValidate.Validator.extend('decimal-negative', {
    getMessage: field => {
        return ('Invalid number only two decimal places')
    },
    validate: value => /^[-+]?\d+(?:\.\d+)?$/.test(value) ///^-?\d{2}(\.\d+)?$/.test(value)
});


VeeValidate.Validator.extend('maxCustom', {
    getMessage: (field, args) => {
        return ('You have exceeded the text limit, which is ' + args + ' characters')
    },
    validate(value, option) {
        if (value.length > parseInt(option[0])) {
            return false;
        }
        else {
            return true;
        }
    }
});

VeeValidate.Validator.extend('minMaxInversion', {
    getMessage: (field, args) => {
        return ('For precission, what if scenarios can only variate budget in a 10%')
    },
    validate(value, option) {
        var id = option[0].split('_'), val_input = 0;
        if (id[1] == 'whatif') {
            val_input = (($('#' + id[0] + '_difference').text() / $('#' + id[0] + '_historical').text()) * 100).toFixed(2)
        }

        if (option[0].indexOf('percent_difference') >= 0 && (parseFloat(value) < -10 || parseFloat(value) > 10)) {
            return false;
        }
        else if (option[0].indexOf('whatif') >= 0 && (parseFloat(val_input) < -10 || parseFloat(val_input) > 10)) {
            return false;
        }
        else {
            return true;
        }
    }
});

VeeValidate.Validator.extend('required', {
    getMessage: field => {
        return ('This field is required')
    },
    validate(value, option) {
        if (value === null || value === undefined || value == '' || value.length <= 0) {
            return false;
        }
        else {
            return true;
        }
    }
});

VeeValidate.Validator.extend('porcentaje', {
    getMessage: field => {
        return ('El porcentaje no puede superar 100%')
    },
    validate(value, option) {
        if (value > 100) {
            return false;
        }
        else {
            return true;
        }
    }
});


VeeValidate.Validator.extend('numeric', {
    getMessage: field => {
        return ('Se ingresaron caracteres invalidos')
    },
    validate: value => /^[0-9]+$/.test(value)
});

VeeValidate.Validator.extend('hours', {
    getMessage: field => {
        return ('Formato correcto debe ser HH:MM')
    },
    validate: (value) => new Promise(resolve => {
        let regex = new RegExp("([0-1][0-9]|2[0-3]):([0-5][0-9])");
        resolve({
            valid: value && regex.test(value)
        });
    })
});

VeeValidate.Validator.extend('hours_format', {
    getMessage: field => {
        return ('Formato correcto debe ser HH:MM')
    },
    validate: (value) => new Promise(resolve => {
        let regex = new RegExp("(\\d{2}):(\\d{2})");
        resolve({
            valid: value && regex.test(value)
        });
    })
});

VeeValidate.Validator.extend('hours_value', {
    getMessage: field => {
        return ('La hora debe estar entre 00:00 y 23:59')
    },
    validate: (value) => new Promise(resolve => {
        let regex = new RegExp("([0-1][0-9]|2[0-3]):([0-5][0-9])");
        resolve({
            valid: value && regex.test(value)
        });
    })
});

VeeValidate.Validator.extend('min_hours', {
    getMessage: (field, [args]) => {
        return ('La hora debe ser superior o igual a ') + args.minTime;
    },
    validate: (value, [args]) => new Promise(resolve => {
        if (args.checkTime && value.match(/^\d{2}:\d{2}$/)) {
            resolve({
                valid: value >= args.minTime,
            });
        } else {
            resolve(true);
        }
    })
});

VeeValidate.Validator.extend('remarks', {
	getMessage: field => {
		return (`Se ingresaron caracteres invalidos`);
	},
  	validate: value => /^[A-Za-z0-9\*\.\-\@\%\?\/\ ]+$/.test(value)
});



VeeValidate.Validator.extend('email_custom', {
    getMessage: field => {
        return (`Dirección de correo electrónico no válida`);
    },
    validate: value => /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))+$/.test(value)
});


