<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios"
import Cookies from 'js-cookie';
import _ from 'lodash'

const medicines = ref([])
const releaseForm = ref([])
const therapeuticActions = ref([])
const medicineToAdd = ref({});
const medicinesToEdit = ref({});


const releaseFormById = computed(() => {
    return _.keyBy(releaseForm.value, x => x.id)
})

const therapeuticActionById = computed(() => {
    return _.keyBy(therapeuticActions.value, x => x.id)
})

async function fetchMedicines() {
    const r = await axios.get("/api/medicines/")
    console.log("Лекарства")
    console.log(r.data)
    medicines.value = r.data
}

async function fetchReleaseForms() {
    const r = await axios.get("/api/forms/")
    console.log("Формы выпуска")
    console.log(r.data)
    releaseForm.value = r.data
}

async function fetchTherapeuticActions() {
    const r = await axios.get("/api/actions/")
    console.log("Терапевтические действия")
    console.log(r.data)
    therapeuticActions.value = r.data
}


async function onLoadClick() {
    await fetchMedicines()
    await fetchReleaseForms()
    await fetchTherapeuticActions()
}

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    await fetchMedicines()
    await fetchReleaseForms()
    await fetchTherapeuticActions()
})

async function onMedicineAdd() {
    const formData = new FormData();

    formData.set('name', medicineToAdd.value.name)
    formData.set('releaseForm', medicineToAdd.value.releaseForm)
    formData.set('therapeuticAction', medicineToAdd.value.therapeuticAction)

    await axios.post("/api/medicines/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchMedicines()
}

async function onRemoveClick(medicine) {
    await axios.delete(`/api/medicines/${medicine.id}/`);
    await fetchMedicines(); // переподтягиваю
}

async function onMedicineEditClick(medicine) {
    medicinesToEdit.value = {
        id: medicine.id,
        name: medicine.name,
        releaseForm: medicine.releaseForm.id,
        therapeuticAction: medicine.therapeuticAction.id,
    };
    console.log(medicinesToEdit.value)
}

async function onUpdateMedicine() {
    
    const formData = new FormData();
    Object.entries(medicinesToEdit.value).forEach(([key, value]) => {
        if(value != null) formData.set(key, value);
    });
    console.log(medicinesToEdit.value);
    try {
        await axios.put(
            `/api/medicines/${medicinesToEdit.value.id}/`,
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
    await fetchMedicines();
}
</script>
<template>
    <form @submit.prevent.stop="onMedicineAdd">
        <div class="row field">
            <div class="col-auto">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input type="text" class="form-control" v-model="medicineToAdd.name" required />
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="medicineToAdd.releaseForm" required>
                        <option :value="g.id" v-for="g in releaseForm">{{ g.form }}</option>
                    </select>
                    <label for="floatingInput">Форма</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="medicineToAdd.therapeuticAction" required>
                        <option :value="g.id" v-for="g in therapeuticActions">{{ g.action }}</option>
                    </select>
                    <label for="floatingInput">Действие</label>
                </div>
            </div>
        </div>
        <div class="row field">
            <div class="col-auto">
                <div class="col-auto">
                    <button class="btn btn-primary">
                        Добавить
                    </button>
                </div>
            </div>
        </div>
    </form>
    <div v-for="item in medicines" class="patient-item">
        <div class="row">
            <div class="col">
                <b>{{ item.name }}</b>
            </div>
            <div class="col">
                <b>{{ item.releaseForm?.form }}</b>
            </div>
            <div class="col">
                <b>{{ item.therapeuticAction?.action }}</b>
            </div>
        </div>
        <button class="btn btn-success red-item" @click="onMedicineEditClick(item)" data-bs-toggle="modal"
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
                                <input type="text" class="form-control" v-model="medicinesToEdit.name" />
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="medicinesToEdit.releaseForm">
                                    <option :value="d.id" v-for="d in releaseForm">
                                        {{ d.form }}
                                    </option>
                                </select>
                                <label for="floatingInput">Форма выпуска</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="medicinesToEdit.therapeuticAction">
                                    <option :value="d.id" v-for="d in therapeuticActions">
                                        {{ d.action }}
                                    </option>
                                </select>
                                <label for="floatingInput">Терапевтическое действие</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateMedicine">
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