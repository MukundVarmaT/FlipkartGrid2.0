import React from 'react'
import Card from './Card'

var data = [
    { position: 'Leader', name: 'Vikas K Mahendar', desc: 'ML Engineer', link: 'https://www.google.com' },
    { position: 'Member', name: 'Mukund Varma T', desc: 'ML God', link: 'https://www.google.com' },
    { position: 'Member', name: 'Mukesh V', desc: 'Web Developer', link: 'https://www.google.com' },
]

function CardGrid() {
    return (
        <footer>
            <div style={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'center',
                bottom: '4px'
            }}>
                {
                    data.map((item, key) => {
                        return <Card data={item} key={key} />
                    })
                }
            </div>
        </footer>
    )
}

export default CardGrid