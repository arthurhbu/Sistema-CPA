import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function SelectAutoWidth({ onSelectChange, label, options, textColor}) {
  const [selectedValue, setSelectedValue] = React.useState('');

  const handleChange = (event) => {
    const value = event.target.value
    setSelectedValue(value);
    onSelectChange(value);
  };

  return (
      <FormControl sx={{ m: 5, minWidth: 130}} style={{width: 'auto', margin: '0', marginTop:'20px'}}>
        <InputLabel id={`select-${label}-label`} sx={{ color: textColor }}>{label}</InputLabel>
        <Select
          labelId={`select-${label}-label`}
          id={`select-${label}`}
          value={selectedValue}
          onChange={handleChange}
          autoWidth={true} 
          label="introConclusao"
          sx={{
            color: textColor,  // Cor do texto do Select
            '&:hover .MuiOutlinedInput-notchedOutline': { // Hover na borda
              borderColor: '#E6E6E6',
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': { // Borda quando o Select está focado
              borderColor: textColor,
            },
            '& .MuiSelect-icon': { color: textColor }, // Cor do ícone do Select
            '& .MuiOutlinedInput-notchedOutline': { borderColor: textColor }, // Cor da borda do Select
          }}
        >
          {options.map(( option) => (
            <MenuItem key={option.value} value={option.value}>
                {option.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
  );
}