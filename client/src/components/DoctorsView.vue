<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios"
import Cookies from 'js-cookie';
import _ from 'lodash'

const doctors = ref([])
const doctorToAdd = ref({});
const doctorToEdit = ref({});

const doctorById = computed(() => {
    return _.keyBy(doctors.value, x => x.id)
})

async function fetchDoctors() {
    const r = await axios.get("/api/doctors/")
    console.log("Врачи")
    console.log(r.data)
    doctors.value = r.data
}


async function onLoadClick() {
    await fetchDoctors()
}

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    await fetchDoctors()
})

async function onDoctorAdd() {
    const formData = new FormData();

    formData.set('name', doctorToAdd.value.name)

    await axios.post("/api/doctors/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchDoctors()
}

async function onRemoveClick(doctor) {
    await axios.delete(`/api/doctors/${doctor.id}/`);
    await fetchDoctors(); // переподтягиваю
}

async function onDoctorEditClick(doctor) {
    doctorToEdit.value = {
        ...doctor,
    };
}

async function onUpdateDoctor() {
    console.log(doctorToEdit)

    const formData = new FormData();
    Object.entries(doctorToEdit.value).forEach(([key, value]) => {
        if (value != null) formData.set(key, value);
    });
    try {
        await axios.put(
            `/api/doctors/${doctorToEdit.value.id}/`,
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            }
        );
    } catch (error) {
        console.error("Ошибка при обновлении записи:", error);
    }
    await fetchDoctors();
}
</script>


<template>
    <form @submit.prevent.stop="onDoctorAdd">
        <div class="row field">
            <div class="col-auto">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input type="text" class="form-control" v-model="doctorToAdd.name" required />
                    <label for="floatingInput">ФИО</label>
                </div>
            </div>
        </div>
        <div class="row field">
            <div class="col-auto">
                <button class="btn btn-primary">
                    Добавить
                </button>
            </div>
        </div>
    </form>
    <div v-for="item in doctors" class="patient-item">
        <div class="row">
            <div class="col ">
                <b>{{ item.name }}</b>
            </div>
        </div>
        <button class="btn btn-success red-item" @click="onDoctorEditClick(item)" data-bs-toggle="modal"
            data-bs-target="#editPatientModal">
            <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger del-item" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
        </button>
    </div>

    <button @click="onLoadClick">Загрузить</button>


    <div class="modal fade" id="editPatientModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактирование
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="doctorToEdit.name" />
                                <label for="floatingInput">Фамилия</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateDoctor">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

</template>


<style lang="scss" scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css");

.patient-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: flex;
    align-items: center;
}

.del-item {
    justify-content: right;
    margin-left: 10px;
}

.red-item {
    justify-content: right;
    margin-left: auto;
}

.navbar-nav {
    justify-content: right;
    margin: 1rem;
}

.field {
    margin-bottom: 10px;
}
</style>
