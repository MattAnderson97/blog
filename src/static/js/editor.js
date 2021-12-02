const editor = new EditorJS({
    holder: 'editorjs',/** 
     * Available Tools list. 
     * Pass Tool's class or Settings object for each Tool you want to use 
     */
    tools: {
        header: Header,
        delimiter: Delimiter,
        paragraph: {
            class: Paragraph,
            inlineToolbar: true,
            config: { 
                placeholder: 'Begin writing your post...',
            },
        },
        embed: Embed,
        image: SimpleImage,
    }
});

$("#publish_btn").click(function(){    
    editor.save().then((outputData) => {
        data = new FormData(document.querySelector('form'));
        data.append('content', JSON.stringify(outputData));

        // xhr = new XMLHttpRequest();
        // xhr.open('POST', '/posts/create/save', true);
        // xhr.setRequestHeader("Content-Type", false);

        // xhr.onreadystatechange = function(){
        //     if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        //         window.location.assign(xhr.responseURL);
        //     }
        // }

        // xhr.send(data);
        $.ajax({
            url: '/posts/create/save',
            data: data,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(event, xhr, settings) {
                window.location.assign(settings.responseText);
            }
        })
    });
});

// changeHandler = function() {
// }