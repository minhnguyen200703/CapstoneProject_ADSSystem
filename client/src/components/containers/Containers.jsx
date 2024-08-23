import { useState, useEffect } from "react";
import containersData from '../../data/containers.json';

export default function Containers() {

    // Containers
    const [selectedContainerItems, setSelectedContainerItems] = useState([]);
    const [isShowingAllContainers, setIsShowingAllContainers] = useState(false);
    const [containerFilter, setContainerFilter] = useState('All'); // 'All', 'Available', 'Unavailable'
    const [allContainersSelected, setAllContainersSelected] = useState(false); // Track if all items are selected

    useEffect(() => {
        // Initialize the state with container data
        const initialContainersData = containersData.map(container => ({
            id: container.CarID,
            isChecked: container.isAvailable,
            ContNumber: container.ContNumber,
            Location: container.Location,
            isAvailable: container.isAvailable
        }));
        setSelectedContainerItems(initialContainersData);
    }, []);

    useEffect(() => {
        // Update the 'allContainersSelected' state whenever 'selectedContainerItems' changes
        const selectedCount = selectedContainerItems.filter(item => item.isChecked).length;
        const availableCount = selectedContainerItems.filter(item => item.isAvailable).length;
        setAllContainersSelected(selectedCount === availableCount && availableCount > 0);
    }, [selectedContainerItems]);

    const handleSelectAll = () => {
        const newSelectionState = !allContainersSelected; // Toggle state
        setSelectedContainerItems(selectedContainerItems.map(item => ({
            ...item,
            isChecked: item.isAvailable && newSelectionState // Toggle based on availability
        })));
    };

    const handleCheckboxChange = (e, id) => {
        const checked = e.target.checked;
        setSelectedContainerItems(selectedContainerItems.map(item =>
            item.id === id ? { ...item, isChecked: checked } : item
        ));
    };

    const handleShowMore = () => {
        setIsShowingAllContainers(true);
    };

    const handleHideMore = () => {
        setIsShowingAllContainers(false);
    };

    const handleContainerFilterChange = (newFilter) => {
        setContainerFilter(newFilter);
        setIsShowingAllContainers(false); // Hide additional items when containerFilter changes
    };

    const containerFilteredContainerItems = selectedContainerItems.filter(item => {
        if (containerFilter === 'Available') return item.isAvailable;
        if (containerFilter === 'Unavailable') return !item.isAvailable;
        return true;
    });

    const displayedItems = isShowingAllContainers ? containerFilteredContainerItems : containerFilteredContainerItems.slice(0, 5);
    console.log(containersData)
    return (
        <section className="containers">
            <h2>Containers</h2>
            <div className="mb-16">
                <button
                    className={`btn btn-md mr-12 ${containerFilter === 'All' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleContainerFilterChange('All')}
                >
                    All
                </button>
                <button
                    className={`btn btn-md mr-12 ${containerFilter === 'Available' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleContainerFilterChange('Available')}
                >
                    Available
                </button>
                <button
                    className={`btn btn-md mr-12 ${containerFilter === 'Unavailable' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleContainerFilterChange('Unavailable')}
                >
                    Unavailable
                </button>
            </div>

            <div className="table-container">
                <table className="custom-table">
                    <thead>
                        <tr>
                            <th>
                                <span
                                    className="select-all-text"
                                    onClick={handleSelectAll}
                                >
                                    {allContainersSelected ? 'Deselect All' : 'Select All'}
                                </span>
                            </th>
                            <th>Status</th>
                            <th>Id</th>
                            <th>Location Id</th>
                        </tr>
                    </thead>
                    <tbody>
                        {displayedItems.map(item => (
                            <tr key={item.id}>
                                <td>
                                    <input
                                        type="checkbox"
                                        checked={item.isChecked}
                                        onChange={(e) => handleCheckboxChange(e, item.id)}
                                        disabled={!item.isAvailable}
                                    />
                                </td>
                                <td>
                                    <span className={`status ${item.isAvailable ? "available" : "unavailable"}`}>{item.isAvailable ? "Available" : "Unavailable"}</span>
                                </td>
                                <td>{`${item.ContNumber}`}</td>
                                <td>{item.Location}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {!isShowingAllContainers && containerFilteredContainerItems.length > 5 && (
                    <div className="show-more flex-align-center flex-justify-center" onClick={handleShowMore} style={{ cursor: 'pointer' }}>
                        <strong className="select-all-text">Show {containerFilteredContainerItems.length - 5} more</strong>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                        </svg>
                    </div>
                )}
                {isShowingAllContainers && (
                    <div className="show-more flex-align-center flex-justify-center" onClick={handleHideMore} style={{ cursor: 'pointer' }}>
                        <strong>Hide {containerFilteredContainerItems.length - 5} more</strong>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5" />
                        </svg>
                    </div>
                )}
            </div>
        </section>
    )
}