<template>
    <div class="studentsGroup-container">
        <Header></Header>
        <div v-if="editGroup == false" class="studentsGroup-container-blocks" style="margin-top: 103px;">
            <div class="studentsGroup-container-blocks-row">
            <div class="students-group-add-button">
                <div class="students-group-add-button-vector" @click="createGroup"></div>
                <div class="students-group-add-button-text">Создать новую группу</div>
            </div>
            </div>
        </div>
        <div v-if="editGroup" class="editGroup-container-blocks">
            <div class="editGroup-container-group-name">Students Group Name</div>
            <div class="editGroup-container-group-selector-buttons">
                <button class="editGroup-container-selector-button"></button>
                <button class="editGroup-container-selector-button"></button>
                <button class="editGroup-container-selector-button"></button>
                <button class="editGroup-container-selector-button"></button>
            </div>
            <div class="editGroup-container-blocks" style="margin-top: 22px;">
            <div class="editGroup-container-blocks-row">
                <div class="edit-group-add-button">
                    <div class="edit-group-add-button-vector"></div>
                    <div class="edit-group-add-button-text">Создать задание</div>
                </div>
            </div>
            </div>
        </div>
    </div>

</template>

<script>
import Header from '../components/HeaderPage.vue'
export default{
    data() {
        return {
            editGroup: false,
            rowFix: 1,
            Groups: {

            }
        }
    },
    components: {
        Header
    },
    methods: {
        createGroup () {
            
            const tableGroup = document.querySelector(".studentsGroup-container-blocks")
            const tableGroupRows = document.querySelectorAll(".studentsGroup-container-blocks-row")
            const tableGroupRow = tableGroupRows[tableGroupRows.length - 1]

            console.log(tableGroupRow)
            const newGroup = document.createElement('div')
            newGroup.className = 'students-group-block'
            const newGroupName = document.createElement('div')
            newGroupName.className = 'students-group-block-name'
            newGroupName.textContent = 'GroupName'
            const newGroupInfo = document.createElement('div');
            newGroupInfo.className = 'students-group-block-info'
            const newGroupOpenButton = document.createElement('button');
            const newGroupInfoCircle = document.createElement('div');
            newGroupInfoCircle.className = 'students-group-block-info-circle';
            const newGroupInfoName = document.createElement('div');
            newGroupInfoName.className = 'students-group-block-info-name'
            newGroupInfoName.textContent = 'Teacher Name'
            newGroupOpenButton.className = 'students-group-block-open-button'
            newGroupOpenButton.textContent = 'Открыть'
            newGroupOpenButton.onclick = () => {
                this.editGroup = true
            }
            console.log(this.editGroup)
            newGroupInfo.append(newGroupInfoCircle, newGroupInfoName);
            newGroup.append(newGroupName, newGroupInfo, newGroupOpenButton)
            //newGroup.click(this.editGroup = true);
            //newGroup.innerHTML = '<div class="students-group-block-name">GoupName</div><div class="students-group-block-info"></div><button class="students-group-block-open-button">Открыть</button>'
            if (this.rowFix < 3){
                if (this.rowFix > 0 ){
                newGroup.style.marginLeft = 57 + 'px'
                }
                tableGroupRow.appendChild(newGroup);
                this.rowFix += 1;

            }
            else{
                this.rowFix = 0;
                const NewRow = document.createElement('div');
                NewRow.className = 'studentsGroup-container-blocks-row';
                NewRow.style.marginTop = 36 + 'px';
                NewRow.appendChild(newGroup);
                tableGroup.appendChild(NewRow);
                this.rowFix += 1;
            }
            
            console.log(tableGroupRow)
            console.log(this.rowFix)
            console.log(newGroup)
        }

    }
}

</script>