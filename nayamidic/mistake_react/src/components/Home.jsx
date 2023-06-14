import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography } from "@mui/material";

export const Home = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/mistake/home/')
            .then(response => {
                setData(response.data);
            });
    }, []);
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', margin: '0 30%' }}>
        {data && data.map(item => (
            <Card key={item.id} style={{ marginBottom: "15px", width: '100%', borderRadius: 15, boxShadow: "0 8px 40px -12px rgba(0,0,0,0.3)" }}>
                <CardContent>
                    <Typography variant="h6" component="h2" style={{fontWeight: "bold"}}>
                        {item.user.username}
                    </Typography>
                    <Typography color="textSecondary" style={{ marginBottom: "10px" }}>
                        Categories: {Array.isArray(item.categories) ? item.categories.join(', ') : item.categories}
                    </Typography>
                    <Typography variant="body2" component="p">
                        {item.text}
                    </Typography>
                </CardContent>
            </Card>
        ))}
    </div>
    );
  };
  
  