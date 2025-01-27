import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText } from '@mui/material';

interface Category {
  id: number;
  name: string;
}

const Categories: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [newCategoryName, setNewCategoryName] = useState<string>('');

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/shop/categories/', {
        withCredentials: true, // Добавляем эту опцию
      });
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleCreateCategory = async () => {
    try {
      await axios.post(
        'http://localhost:8000/api/shop/categories/',
        { name: newCategoryName },
        { withCredentials: true } // Добавляем эту опцию
      );
      setNewCategoryName('');
      fetchCategories();
    } catch (error) {
      console.error('Error creating category:', error);
    }
  };

  return (
    <Container sx={{ mt: 5 }}>
      <Typography variant="h5" gutterBottom component="div">
      List of categories
      </Typography>
      <List>
        {categories.map((category) => (
          <ListItem key={category.id} component="div" disablePadding>
            <ListItemText primary={category.name} />
          </ListItem>
        ))}
      </List>
      <div>
        <TextField
          label="New category"
          variant="outlined"
          fullWidth
          value={newCategoryName}
          onChange={(e) => setNewCategoryName(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Button variant="contained" onClick={handleCreateCategory}>
        Create a category
        </Button>
      </div>
    </Container>
  );
};

export default Categories;
