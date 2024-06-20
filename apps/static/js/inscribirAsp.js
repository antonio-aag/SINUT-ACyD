document.addEventListener('DOMContentLoaded', function () {
    /**Establecer valores según el registro en la BD */   
    var estadoCivilBD = document.getElementById('estadoCivilBD').value;
    document.getElementById('estadoCivil').value = estadoCivilBD;
    var carrera1BD = document.getElementById('carrera1BD').value;
    var carrera1 = document.getElementById('carrera1');
    for (var i = 0; i < carrera1.options.length; i++) {
        if (carrera1.options[i].value === carrera1BD) {
            carrera1.selectedIndex = i;
            break;
        }
    }

    const checkbox1 = document.getElementById('acta');
    checkbox1.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;
        } else {
            this.value = 0;
        }
    });

    const checkbox2 = document.getElementById('curpDoc');
    checkbox2.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;
        } else {
            this.value = 0;
        }
    });

    const checkbox3 = document.getElementById('foto');
    checkbox3.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;
        } else {
            this.value = 0;
        }
    });

    const checkbox4 = document.getElementById('certificado');
    checkbox4.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;
        } else {
            this.value = 0;
        }
    });

    const checkbox5 = document.getElementById('constancia');
    checkbox5.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;
        } else {
            this.value = 0;
        }

    });
    
});