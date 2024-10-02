// const [files, setFiles] = useState([])

// const onDrop = useCallback(acceptedFiles => {
//     if(acceptedFiles?.length) { 
//         console.log(acceptedFiles)
//     }
// }, [])

// const {
//     getRootProps, 
//     acceptedFiles,
//     getInputProps,
//     isFocused, 
//     isDragAccept,
//     isDragReject,
// } = useDropzone({ 
//         onDrop , 
//         maxFiles: 1, 
//         accept: {
//             'text/csv': ['.csv'],
//             'application/csv': [],
//             'text/x-csv': [],
//             'text/comma-separated-values': [],
//             'text/x-comma-separated-values': []
//         }})



// function styledDropzone(props){ 
//     const style = useMemo(() => ({
//         ...styles.procurarArquivoBox,
//         ...(isFocused ? styles.focusedDropZone : {}),
//         ...(isDragAccept ? styles.acceptDropZone : {}),
//         ...(isDragReject ? styles.rejectDropZone: {})
//     }), [
//         isFocused,
//         isDragAccept,
//         isDragReject
//     ]);
// }