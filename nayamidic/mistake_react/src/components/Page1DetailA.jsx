import React, { useEffect, useState } from 'react';
import axios from 'axios';

export const Page1DetailA = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/mistake/Post/')
            .then(response => {
                setData(response.data);
            });
    }, []);
    return (
        <div>
            {data && data.map(item => (
                <div key={item.id}>{item.text}{item.id}</div>  // replace `id` and `name` with actual data fields
            ))}
        </div>
    );
  };
  