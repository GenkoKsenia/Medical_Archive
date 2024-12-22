<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios"
import Cookies from 'js-cookie';
import _ from 'lodash'

const patients = ref([])
const medicines = ref([])
const doctors = ref([])
const patientToAdd = ref({});
const patientToEdit = ref({});
const patientsPictureRef = ref();
const patientAddImageUrl = ref();

const medicineById = computed(() => {
    return _.keyBy(medicines.value, x => x.id)
})

const doctorById = computed(() => {
    return _.keyBy(doctors.value, x => x.id)
})

async function fetchPatients() {
    const r = await axios.get("/api/patients/")
    console.log("Пациенты")
    console.log(r.data)
    patients.value = r.data
}

async function fetchMedicines() {
    const r = await axios.get("/api/medicines/")
    console.log("Лекарства")
    console.log(r.data)
    medicines.value = r.data
}

async function fetchDoctors() {
    const r = await axios.get("/api/doctors/")
    console.log("Врачи")
    console.log(r.data)
    doctors.value = r.data
}


async function onLoadClick() {
    await fetchPatients()
    await fetchMedicines()
    await fetchDoctors()
}

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    await fetchPatients()
    await fetchMedicines()
    await fetchDoctors()
})

async function onPatientAdd() {
    const formData = new FormData();

    if (patientsPictureRef.value.files.length > 0)
        formData.append('picture', patientsPictureRef.value.files[0]);

    formData.set('lastName', patientToAdd.value.lastName)
    formData.set('firstName', patientToAdd.value.firstName)
    formData.set('number', patientToAdd.value.number)
    formData.set('dateBirth', patientToAdd.value.dateBirth)
    formData.set('patronymic', patientToAdd.value.patronymic)
    formData.set('medicine', patientToAdd.value.medicine)
    formData.set('doctor', patientToAdd.value.doctor)

    await axios.post("/api/patients/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchPatients()
}

async function patientAddPictureChange() {
    patientAddImageUrl.value = URL.createObjectURL(patientsPictureRef.value.files[0])
}

async function onRemoveClick(patient) {
    await axios.delete(`/api/patients/${patient.id}/`);
    await fetchPatients(); // переподтягиваю
}

async function onPatientEditClick(patient) {
    patientToEdit.value = {
        ...patient,
        doctor: patient.doctor.id,
        medicine: patient.medicine.id,
    };
}

async function onUpdatePatient() {
    console.log(patientToEdit)

    if (typeof patientToEdit.value.picture === "string") {
        const response = await fetch(patientToEdit.value.picture);
        const blob = await response.blob();
        const file = new File([blob], "existing-image.jpg", {
            type: blob.type,
        });
        patientToEdit.value.picture = file;
    }
    const formData = new FormData();
    Object.entries(patientToEdit.value).forEach(([key, value]) => {
        if (key != "picture" && value != null) {
            formData.set(key, value);
            console.log(key, value)
        }
    });

    if (patientToEdit.value.picture != undefined)
        formData.append("picture", patientToEdit.value.picture);

    try {
        await axios.put(
            `/api/patients/${patientToEdit.value.id}/`,
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
    clearDataImage();
    await fetchPatients();
}

const patientEditPictureChange = (event) => {
    patientToEdit.value.picture = event.target.files[0];
    dataItemImageEditShow.value = URL.createObjectURL(
        patientToEdit.value.picture
    );

    console.log(event.target.files[0])
};

const modalImage = ref(null);
const isImageFullScreen = ref(false);

function openFullScreen(imageUrl) {
    modalImage.value = imageUrl;
    isImageFullScreen.value = true;
}

function closeFullScreen() {
    isImageFullScreen.value = false;
}

const dataItemImageEditShow = ref()

async function clearDataImage() {
    console.log("patientToEdit.value.picture")
    console.log(patientToEdit.value.picture)
    dataItemImageEditShow.value = null
    console.log(patientToEdit.value.picture)
    console.log("patientToEdit.value.picture")

}

async function downloadExcel() {
    try {
        const response = await axios.get(`/api/patients/export-excel/`, {
            responseType: "blob", // Указываем, что ожидаем бинарные данные
        });

        // Создаем URL для скачивания файла
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;

        // Указываем имя файла
        const contentDisposition = response.headers["content-disposition"];
        const filename = contentDisposition
            ? contentDisposition.split("filename=")[1]
            : "file.xlsx";

        link.setAttribute("download", filename.replace(/"/g, ""));
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error("Ошибка при скачивании файла Excel:", error);
    }
}
</script>


<template>
    <form @submit.prevent.stop="onPatientAdd">
        <div class="row field">
            <div class="row row-item">
                <div class="col-auto">
                    <div class="form-floating">
                        <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                        <input type="text" class="form-control" v-model="patientToAdd.lastName" required />
                        <label for="floatingInput">Фамилия</label>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="patientToAdd.firstName" required />
                        <label for="floatingInput">Имя</label>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="patientToAdd.patronymic" required />
                        <label for="floatingInput">Отчество</label>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="patientToAdd.dateBirth" required />
                        <label for="floatingInput">Дата рождения</label>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="patientToAdd.number" required />
                        <label for="floatingInput">Номер телефона</label>
                    </div>
                </div>
            </div>
            <div class="row row-item">
                <div class="col-auto">
                    <div class="form-floating">
                        <select class="form-select" v-model="patientToAdd.medicine" required>
                            <option :value="g.id" v-for="g in medicines">{{ g.name }}</option>
                        </select>
                        <label for="floatingInput">Лекарство</label>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="form-floating">
                        <select class="form-select" v-model="patientToAdd.doctor" required>
                            <option :value="g.id" v-for="g in doctors">{{ g.name }}</option>
                        </select>
                        <label for="floatingInput">Врач</label>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="col-auto">
                        <input class="form-control" type="file" ref="patientsPictureRef"
                            @change="patientAddPictureChange">
                    </div>
                    <div class="col-auto">
                        <img :src="patientAddImageUrl" style="max-height: 60px;" alt="">
                    </div>
                </div>
            </div>
            <div class="row row-item">
                <div class="col-auto">
                    <button class="btn btn-primary">
                        Добавить
                    </button>
                </div>
            </div>
        </div>
    </form>
    <div class="row row-item">
        <div class="col-auto">
            <button class="btn btn-danger" @click="downloadExcel">
                Скачать
            </button>
        </div>
    </div>
    <div v-for="item in patients" class="patient-item">
        <div class="row">
            <div class="col item-info" v-show="item.picture">
                <img :src="item.picture" style="max-height:60px;" @click="openFullScreen(item.picture)"><br />
                <div v-if="isImageFullScreen" class="fullscreen-overlay" @click="closeFullScreen">
                    <img :src="modalImage" class="fullscreen-image" alt="Увеличенное изображение">
                </div>
            </div>
            <div class="col item-info">
                <b>{{ item.lastName }}</b>
            </div>
            <div class="col item-info">
                <b>{{ item.firstName }}</b>
            </div>
            <div class="col item-info">
                <b>{{ item.patronymic }}</b>
            </div>
            <div class="col item-info">
                <b>{{ item.medicine?.name || 'Не указано' }}</b>
            </div>
        </div>
        <button class="btn btn-success red-item" @click="onPatientEditClick(item)" data-bs-toggle="modal"
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
                                <input type="text" class="form-control" v-model="patientToEdit.lastName" />
                                <label for="floatingInput">Фамилия</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="patientToEdit.firstName" />
                                <label for="floatingInput">Имя</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="patientToEdit.patronymic" />
                                <label for="floatingInput">Отчество</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="patientToEdit.dateBirth" />
                                <label for="floatingInput">Дата рождения</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="patientToEdit.number" />
                                <label for="floatingInput">Номер телефона</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="patientToEdit.medicine">
                                    <option :value="m.id" v-for="m in medicines">
                                        {{ m.name }}
                                    </option>
                                </select>
                                <label for="floatingInput">Лекарство</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="patientToEdit.doctor">
                                    <option :value="d.id" v-for="d in doctors">
                                        {{ d.name }}
                                    </option>
                                </select>
                                <label for="floatingInput">Врач</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <input class="form-control" type="file" @change="patientEditPictureChange" />
                        </div>
                        <div class="col-auto">
                            <img :src="dataItemImageEditShow || patientToEdit.picture" style="max-height: 60px;"
                                alt="Предпросмотр изображения" />
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="clearDataImage">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdatePatient">
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

.fullscreen-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.fullscreen-image {
    max-width: 90%;
    max-height: 90%;
    object-fit: contain;
    cursor: pointer;
}

.item-info {
    width: 150px;
}

.row-item {
    margin-bottom: 10px;
}
</style>
