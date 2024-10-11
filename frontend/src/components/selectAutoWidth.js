import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function SelectAutoWidth({ onSelectChange, label, options}) {
  const [selectedValue, setSelectedValue] = React.useState('');

  const handleChange = (event) => {
    const value = event.target.value
    setSelectedValue(value);
    onSelectChange(value);
  };

  return (
    <div>
      <FormControl sx={{ m: 5, minWidth: 130 }} style={{margin: '0', marginTop:'20px'}}>
        <InputLabel id={`select-${label}-label`}>{label}</InputLabel>
        <Select
          labelId={`select-${label}-label`}
          id={`select-${label}`}
          value={selectedValue}
          onChange={handleChange}
          autoWidth
          label="introConclusao"
        >
          {options.map(( option) => (
            <MenuItem key={option.value} value={option.value}>
                {option.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
}