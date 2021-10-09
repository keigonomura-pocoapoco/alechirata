$(function(){
    const actualBtn = document.getElementById('pictures');

    const fileChosen = document.getElementById('file-chosen');

    actualBtn.addEventListener('change', function(){
        if (this.files.length == 1){
            if (this.files[0].name.length > 25){
                let pic_name = this.files[0].name.substring(0, 20);
                let where_the_dot = this.files[0].name.indexOf('.');
                let last_letters = this.files[0].name.substring(where_the_dot - 3, where_the_dot);
                let file_type = this.files[0].name.substring(where_the_dot);
                fileChosen.textContent = pic_name + '...' + last_letters + file_type;
            } else {
                fileChosen.textContent = this.files[0].name;
            }
        } else {
            fileChosen.textContent = this.files.length + " files are selected.";
        }
    })
});