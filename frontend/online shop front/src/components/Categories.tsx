import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Category {
  id: number;
  name: string;
}

const Categories: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [newCategoryName, setNewCategoryName] = useState<string>('');
  
  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/shop/categories/');
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
      await axios.post('http://localhost:8000/api/shop/categories/', {
        name: newCategoryName,
      });
      setNewCategoryName('');
      fetchCategories();
    } catch (error) {
      console.error('Error creating category:', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2>List of categories</h2>
      <ul>
        {categories.map((category) => (
          <li key={category.id}>{category.name}</li>
        ))}
      </ul>
      <div className="mb-3">
        <label htmlFor="newCategoryName" className="form-label">New category</label>
        <input
          type="text"
          className="form-control"
          id="newCategoryName"
          value={newCategoryName}
          onChange={(e) => setNewCategoryName(e.target.value)}
        />
      </div>
      <button
        className="btn btn-primary"
        onClick={handleCreateCategory}
      >
        Create a category
      </button>
    </div>
  );
};

export default Categories;
