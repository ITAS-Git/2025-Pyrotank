# Project Synopsis

## Project Management Methodology

Our group followed the **Kanban methodology** using GitHub Projects. We created various issues representing individual tasks required to complete the project. The Kanban board included six key sections:

- **Backlog**
- **Ready**
- **In Progress**
- **In Review**
- **Done**
- **Paused**

Tasks were added to the backlog at the start of each cycle with the goal of completing them by the end of the sprint. However, some tasks had to be moved into the Paused section due to project complications. Ultimately, all tasks progressed through the board and were completed, ending in the Done column.

---

## Reasons for Scope Changes

There were two main reasons for changes in project scope:

1. **Time Constraints**  
   Due to limited time, we had to remove some planned features such as a second tank and multiple game modes.

2. **Budget Limitations**  
   From the start, our budget made it clear that implementing two tanks would be unfeasible. This led us to pivot toward a **target shooting game** instead.

---

## Things That Were Left Undone

A few features were not completed due to time constraints:

- **Laser Accuracy**  
  The laser works, but it is difficult to aim. Focusing the laser beam would have improved precision.

- **Target Wiring Protection**  
  The backs of the targets were left exposed. While not essential, this makes the system unsuitable for outdoor use.

- **Powering the Raspberry Pi**  
  Currently, the tank must be opened to turn on the Raspberry Pi. We intended to create a more accessible way to power it on/off without removing the tank body.

---

## Lessons Learned

This project taught us valuable lessons, including:

- The importance of **time management**
- The need for **adjusting scope** as circumstances change

---

## Good Points / Bad Points

### ✅ Good Points

- **Laser + Light Sensor Integration**  
  Replacing the IR cannon with a laser and light sensor dramatically increased shooting and hit detection accuracy.

- **Headless Tank Operation**  
  Running the tank script as a boot service enabled the Raspberry Pi to function without a monitor or keyboard. While occasionally finicky, it streamlined the overall user experience.

### ❌ Drawbacks

- **Light Sensor Sensitivity**  
  The targets can be triggered by strong external light sources, though rare, this remains a potential issue.

- **Unfinished LED Display**  
  We were unable to fully implement the LED display on the tank. Instead, we created a software-based version that runs on a computer. It's functional but not integrated into the physical system.
