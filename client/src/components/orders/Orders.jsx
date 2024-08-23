import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ordersData from '../../data/orders.json';

export default function Orders() {

    // Orders
    const [selectedOrderItems, setSelectedOrderItems] = useState([]);
    const [isShowingAllOrders, setIsShowingAllOrders] = useState(false);
    const [orderFilter, setOrderFilter] = useState('All'); // 'All', 'Pending', 'Finished'
    const [allOrdersSelected, setAllOrdersSelected] = useState(false); // Track if all items are selected

    useEffect(() => {
        // Initialize the state with order data
        const initialOrdersData = ordersData.map(order => ({
            id: order.OrderID,
            isChecked: order.CurrentStatus == "Pending",
            type: order.OrderType,
            Book_LiftingEmpty: order.Book_LiftingEmpty,
            Book_CutOffDate: order.Book_CutOffDate,
            Bill_LastFreeDayDEM: order.Bill_LastFreeDayDEM,
            Bill_LastFreeDayDET: order.Bill_LastFreeDayDET,
            orderId: order.ContNumber,
            source: order.Locations[0],
            destination: order.Locations[1],
            isPending: order.CurrentStatus == "Pending"
        }));
        setSelectedOrderItems(initialOrdersData);
    }, []);

    useEffect(() => {
        // Update the 'allOrdersSelected' state whenever 'selectedOrderItems' changes
        const selectedCount = selectedOrderItems.filter(item => item.isChecked).length;
        const availableCount = selectedOrderItems.filter(item => item.isPending).length;
        setAllOrdersSelected(selectedCount === availableCount && availableCount > 0);
    }, [selectedOrderItems]);

    const handleSelectAll = () => {
        const newSelectionState = !allOrdersSelected; // Toggle state
        setSelectedOrderItems(selectedOrderItems.map(item => ({
            ...item,
            isChecked: item.isPending && newSelectionState // Toggle based on availability
        })));
    };

    const handleCheckboxChange = (e, id) => {
        const checked = e.target.checked;
        setSelectedOrderItems(selectedOrderItems.map(item =>
            item.id === id ? { ...item, isChecked: checked } : item
        ));
    };

    const handleShowMore = () => {
        setIsShowingAllOrders(true);
    };

    const handleHideMore = () => {
        setIsShowingAllOrders(false);
    };

    const handleOrderFilterChange = (newFilter) => {
        setOrderFilter(newFilter);
        setIsShowingAllOrders(false); // Hide additional items when orderFilter changes
    };

    const orderFilteredOrderItems = selectedOrderItems.filter(item => {
        if (orderFilter === 'Pending') return item.isPending;
        if (orderFilter === 'Finished') return !item.isPending;
        return true;
    });

    const displayedItems = isShowingAllOrders ? orderFilteredOrderItems : orderFilteredOrderItems.slice(0, 5);
    console.log(ordersData)
    return (
        <section className="orders">
            <h2>Orders</h2>
            <div className="mb-16 flex-align-center">

                <button
                    className={`btn btn-md mr-12 ${orderFilter === 'All' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleOrderFilterChange('All')}
                >
                    All
                </button>
                <button
                    className={`btn btn-md mr-12 ${orderFilter === 'Pending' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleOrderFilterChange('Pending')}
                >
                    Pending
                </button>
                <button
                    className={`btn btn-md mr-12 ${orderFilter === 'Finished' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleOrderFilterChange('Finished')}
                >
                    Finished
                </button>
            </div>

            <div className="table-container scroll-order ">
                <table className="custom-table">
                    <thead>
                        <tr>
                            <th>
                                <span
                                    className="select-all-text"
                                    onClick={handleSelectAll}
                                >
                                    {allOrdersSelected ? 'Deselect All' : 'Select All'}
                                </span>
                            </th>
                            <th>Status</th>
                            <th>Type</th>
                            <th>Id</th>
                            <th>Source</th>
                            <th>Destination</th>
                            <th>Book_LiftingEmpty</th>
                            <th>Book_CutOffDate</th>
                            <th>Bill_LastFreeDayDEM</th>
                            <th>Bill_LastFreeDayDET</th>

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
                                        disabled={!item.isPending}
                                    />
                                </td>
                                <td>
                                    <span className={`status ${item.isPending ? "available" : "unavailable"}`}>{item.isPending ? "Pending" : "Finished"}</span>
                                </td>
                                <td>{item.type}</td>
                                <td>{`0${item.id}`}</td>
                                <td>{item.source}</td>
                                <td>{item.destination}</td>
                                <td>{item.Book_LiftingEmpty || "-"}</td>
                                <td>{item.Book_CutOffDate || "-"}</td>
                                <td>{item.Bill_LastFreeDayDEM || "-"}</td>
                                <td>{item.Bill_LastFreeDayDET || "-"}</td>

                            </tr>
                        ))}
                    </tbody>
                </table>
                {!isShowingAllOrders && orderFilteredOrderItems.length > 5 && (
                    <div className="show-more flex-align-center flex-justify-center" onClick={handleShowMore} style={{ cursor: 'pointer' }}>
                        <strong className="select-all-text">Show {orderFilteredOrderItems.length - 5} more</strong>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                        </svg>
                    </div>
                )}
                {isShowingAllOrders && (
                    <div className="show-more flex-align-center flex-justify-center" onClick={handleHideMore} style={{ cursor: 'pointer' }}>
                        <strong>Hide {orderFilteredOrderItems.length - 5} more</strong>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5" />
                        </svg>
                    </div>
                )}
            </div>
        </section>
    )
}