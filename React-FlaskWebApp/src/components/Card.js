import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
    Card,
    CardContent,
    Typography
} from '@material-ui/core';


const useStyles = makeStyles({
    root: {
        minWidth: 320,
        margin: '10px',
        backgroundColor: '#047BD5'
    },
    rootLeader: {
        minWidth: 320,
        margin: '10px',
        backgroundColor: 'green'
    },
    title: {
        fontSize: 14,
        fontFamily: 'Riona Sans,sans-serif',
        color: 'white'
    },
    name: {
        fontFamily: 'Riona Sans,sans-serif',
        color: 'white'
    },
    desc: {
        fontFamily: 'Riona Sans,sans-serif',
        color: 'white'
    },
    btn: {
        fontFamily: 'Riona Sans,sans-serif',
        color: 'white'
    }
});

function CardTemplate(props) {
    const classes = useStyles();

    return (
        <Card className={props.data.position === "Leader" ? classes.rootLeader : classes.root} variant="outlined">
            <CardContent>
                <Typography className={classes.title} color="textSecondary" gutterBottom>
                    {props.data.position}
                </Typography>
                <Typography className={classes.name} variant="h5" component="h2">
                    {props.data.name}
                </Typography>
                <Typography className={classes.desc} variant="body2" component="p">
                    {props.data.phone}
                    <br />
                </Typography>
                <Typography className={classes.desc} variant="body2" component="p">
                    {props.data.link}
                <br />
                </Typography>
            </CardContent>
        </Card>
    );
}

export default CardTemplate