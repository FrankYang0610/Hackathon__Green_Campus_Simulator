#
# GREEN CAMPUS SIMULATOR
#
# REN YIXIAO, YANG XIKUN
#
# A HACKATHON PROJECT
#

# IMPORTS
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QListWidget, QListWidgetItem, QPushButton, QRadioButton, QSpacerItem, QSizePolicy, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPainter, QPen, QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.ticker as ticker
import sys, random
from functools import partial

class Image_Template(QLabel):
    def __init__(self, image_path, fixed_height):
        super().__init__()
        self.original_pixmap = QPixmap(image_path)
        self.setFixedSize((int)(self.original_pixmap.width() * (fixed_height / self.original_pixmap.height())),
                          fixed_height)
        self.update_pixmap()

    def update_pixmap(self):
        scaled_pixmap = self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(2, 2, self.width() - 4, self.height() - 4)

class Figure_Template(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_alpha(0.0)
        self.axes = fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.xaxis.set_major_locator(ticker.MultipleLocator(1))
        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(10))
        super(Figure_Template, self).__init__(fig)

class QListWidget_New(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.clearSelection()
            self.selectionModel().clearCurrentIndex()
        else:
            super().mousePressEvent(event)

class Action:
    def __init__(self, name, implement_month, starting_month, cost, carbon_reducing):
        self.name = name
        self.implement_month = implement_month
        self.starting_month = starting_month
        self.cost = cost
        self.carbon_reducing = carbon_reducing

# MAIN WINDOW
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # GLOBAL GAME VARIABLES
        self.current_game_time = 0
        self.max_game_time = 12 * 2 # 2 years
        self.game_started = False
        self.game_over = False
        self.game_budget_count = 0
        self.monthly_invest = 5
        self.ongoing_actions = [Action("DEFAULT", 0, 0, 0, 0)]  # ACTION NAME, ACTION IMPLEMENT MONTH, ACTION COST
        self.carbon_emission_time_series = [0]
        self.carbon_emission_data = [100]
        ######
        self.map_and_curve_maximum_height = 510

        # ACTIONS
        self.Action_Plant_Plants_Near_Car_Road = QRadioButton("Plant plants near car road")
        self.Action_Plant_Plants_Near_Car_Road.toggled.connect(partial(self.update_action_information,
                                                                      f"Planting plants near car roads helps reduce carbon emissions primarily because plants absorb carbon dioxide, a major greenhouse gas, from the air during photosynthesis. This natural process helps mitigate pollution from vehicle emissions, improving air quality and contributing to climate change mitigation by storing carbon in biomass and soil.\n\n"
                                                                      f"Cost: $$ 10, need 3 months to start."))
        ######
        self.Action_Build_Carpark = QRadioButton("Build carpark")
        self.Action_Build_Carpark.toggled.connect(partial(self.update_action_information,
                                                          f"The implementation of a carpark in a school setting is a complex measure with potential to both increase and decrease carbon emissions. On one hand, constructing a carpark can encourage more people to drive to school, potentially increasing the total number of vehicle trips and thus carbon emissions. This is particularly true if public transport options are available but underutilized.\n\n"
                                                          f"On the other hand, a well-planned carpark can reduce emissions if it incorporates features like carpool-only spaces or charging stations for electric vehicles. By incentivizing carpooling, the carpark could reduce the number of vehicles on the road. Additionally, supporting electric vehicles helps shift away from fossil fuels.\n\n"
                                                          f"Overall, the impact of building a carpark on carbon emissions largely depends on its design and the transportation habits it promotes. Without measures to encourage low-carbon transportation options, simply adding more parking space could lead to an increase in carbon emissions.\n\n"
                                                          f"Cost: $$ 20, need 3 months to start."))
        ######
        self.Action_Use_Reflective_Insulation_Coating = QRadioButton("Use neflective insulation coating for main buildings")
        self.Action_Use_Reflective_Insulation_Coating.toggled.connect(partial(self.update_action_information,
                                                                              f"Applying reflective insulation coating to the main buildings of a school can effectively reduce carbon emissions by enhancing the buildings' thermal efficiency. This type of coating is designed to reflect solar radiation, thereby reducing the amount of heat absorbed by the building. As a result, the internal temperatures of the buildings are kept cooler during hot weather, reducing the need for air conditioning. This leads to a decrease in energy consumption, which directly correlates to lower carbon emissions. Additionally, during colder months, reflective insulation helps retain heat inside the building, minimizing the heating requirements and further conserving energy. Overall, the use of reflective insulation coating is a cost-effective measure to improve energy efficiency in school buildings, reducing both energy costs and environmental impact."))
        ######
        self.Action_Use_Nano_Ceramic_Coating = QRadioButton("Use nano ceramic coating for main buildings")
        self.Action_Use_Nano_Ceramic_Coating.toggled.connect(partial(self.update_action_information,
                                                                     f"Applying nano ceramic coatings to the main buildings of a school can significantly lower carbon emissions by improving the buildings' energy efficiency. These coatings are designed to reflect ultraviolet and infrared light, reducing heat absorption and thereby lowering the temperature inside the buildings. This reduction in internal heat decreases the need for air conditioning during warmer months, leading to substantial energy savings and reduced carbon emissions. In addition to cooling benefits, nano ceramic coatings can also add a layer of durability and weather resistance to building exteriors, potentially lessening maintenance needs and extending the lifespan of the building materials. Overall, the implementation of nano ceramic coatings is a practical approach to enhance energy efficiency in school buildings, directly contributing to sustainability goals by reducing energy consumption and carbon footprint."))
        ######
        self.Action_Use_Phase_Change_Material = QRadioButton("Use phase change material (PCM) for main buildings")
        self.Action_Use_Phase_Change_Material.toggled.connect(partial(self.update_action_information,
                                                                      f"Using phase change materials (PCMs) in the main buildings of a school can significantly reduce carbon emissions by enhancing thermal regulation and decreasing the reliance on heating and cooling systems. PCMs absorb excess heat when temperatures rise and release it as temperatures drop, which stabilizes indoor climates and reduces the energy required for temperature control. This leads to a direct reduction in energy consumption and carbon emissions, particularly in regions with significant temperature fluctuations. The effectiveness of PCMs, therefore, contributes to both energy savings and environmental sustainability in school infrastructure."))
        ######
        self.Action_Use_Silicate_Insulation_Coating = QRadioButton("Use silicate insulation coating for main buildings")
        self.Action_Use_Silicate_Insulation_Coating.toggled.connect(partial(self.update_action_information,
                                                                            f"Using silicate insulation coating on the main buildings of a school can be an effective method to reduce carbon emissions by improving the buildings' energy efficiency. Silicate coatings are known for their excellent thermal insulation properties, which help in minimizing heat transfer through the building envelope. This means that during warmer months, the buildings require less air conditioning to maintain comfortable indoor temperatures, and during colder months, less heating is required.\n\n"
                                                                            f"The reduced demand for heating and cooling directly translates into lower energy consumption. Since energy production, especially in regions dependent on fossil fuels, is a major source of carbon emissions, reducing energy consumption effectively cuts down on these emissions. Additionally, silicate coatings are durable and provide added benefits such as fire resistance and protection against moisture, which can prolong the lifespan of building materials and reduce the need for frequent renovations or repairs.\n\n"
                                                                            f"Overall, applying silicate insulation coating to school buildings not only contributes to significant energy savings but also supports sustainability by reducing the carbon footprint associated with building operation and maintenance."))
        ######
        self.Action_Use_Solar_Panels_Minor = QRadioButton("Arrange solar panels for some buildings")
        self.Action_Use_Solar_Panels_Minor.toggled.connect(partial(self.update_action_information,
                                                                   f"Installing solar panels on some of the buildings in a school can be a strategic and cost-effective approach to reducing carbon emissions. By choosing buildings that receive ample sunlight and have suitable roof structures, the school can maximize the efficiency of the solar panels. This partial implementation allows the school to take a significant step towards sustainability, reducing reliance on non-renewable energy sources and cutting down on carbon emissions proportionally to the amount of electricity generated by the solar panels. This can also serve as a pilot project to assess the viability and performance of solar energy within the school premises before a full-scale rollout."))
        ######
        self.Action_Use_Solar_Panels_Major = QRadioButton("Arrange solar panels for all buildings")
        self.Action_Use_Solar_Panels_Major.toggled.connect(partial(self.update_action_information,
                                                                   f"Arranging solar panels for all buildings in a school maximizes the potential for energy generation and carbon emission reduction. This comprehensive approach ensures that every suitable surface contributes to energy production, drastically cutting down the school's dependence on external, possibly non-renewable, energy sources. With a full implementation, the school could potentially reach a net-zero energy consumption level or even become an energy-positive entity, whereby excess energy could be sold back to the grid, further enhancing sustainability goals. However, this approach requires a more significant initial investment and logistical planning but offers the greatest impact in terms of energy savings and environmental benefits."))
        ######
        self.Action_Use_Hollow_Glass_Microsphere_Coating = QRadioButton("Use hollow glass microsphere coating for main buildings")
        ######
        self.Action_Use_Vacuum_Insulation_Coating = QRadioButton("Use vacuum insulation coating for main buildings")
        ######
        self.Action_Use_Polyurethane_Foam_Coating = QRadioButton("Use polyurethane foam coating for main buildings")
        ######
        self.Action_Use_Infrared_Reflective_Coating = QRadioButton("Use infrared reflective coating for main buildings")
        ######
        self.Action_Use_Florocarbon_Coating = QRadioButton("Use florocarbon coating for main buildings")
        ######
        self.Action_Use_Graphene_Insulation_Coating = QRadioButton("Use graphene insulation coating for main buildings")
        ######
        self.Action_Arrange_More_Effective_LED = QRadioButton("Arrange more effective LED for main buildings")
        self.Action_Arrange_More_Effective_LED.toggled.connect(partial(self.update_action_information,
                                                                       f"Implementing high-efficiency LED lighting in the main buildings of a school represents a strategic approach to significantly reduce energy consumption and associated carbon emissions. LEDs are acknowledged for their superior energy efficiency, consuming approximately 75% less energy than traditional incandescent lighting and lasting up to 25 times longer. By transitioning to LED lighting, the school can achieve substantial reductions in electricity demand, directly translating into lower utility costs and a decreased carbon footprint. Furthermore, LEDs offer improved lighting quality, which can enhance the learning environment and potentially boost student productivity and safety. This transition not only aligns with environmental sustainability goals but also represents a prudent financial investment, as the reduced energy costs typically offset the initial installation expenses over time. Therefore, upgrading to LED lighting is not merely an operational improvement but a significant step towards institutional sustainability and fiscal responsibility."))
        ######
        self.Action_Arrange_Smart_Thermostats = QRadioButton("Arrange smart thermostats for main buildings")
        self.Action_Arrange_Smart_Thermostats.toggled.connect(partial(self.update_action_information,
                                                                      f"Implementing smart thermostats in the main buildings of a school can lead to significant energy savings and a corresponding reduction in carbon emissions. By leveraging advanced algorithms and occupancy sensors, smart thermostats optimize HVAC operations, potentially reducing energy usage by approximately 10 to 12 percent for heating and about 15 percent for cooling, according to data from the U.S. Environmental Protection Agency (EPA). This translates into both direct cost savings on utility bills and a substantial decrease in energy consumption, which is critical for institutions aiming to meet sustainability targets. Furthermore, the integration of smart thermostats can contribute towards achieving LEED certification points, enhancing the building's environmental credentials and demonstrating a commitment to sustainable practices. Overall, the data supports that smart thermostats not only offer economic benefits through operational efficiencies but also play a crucial role in reducing the environmental impact of educational facilities."))
        ######
        self.Action_Arrange_High_Performance_Windows = QRadioButton("Arrange high performance windows for main buildings")
        self.Action_Arrange_High_Performance_Windows.toggled.connect(partial(self.update_action_information,
                                                                             f"Installing high-performance windows in the main buildings of a school can dramatically enhance the building's energy efficiency and contribute to substantial reductions in energy costs and carbon emissions. According to studies conducted by the U.S. Department of Energy, high-performance windows can reduce energy loss by up to 30-50%, depending on the existing window type they replace. This reduction in energy loss not only translates into lower heating and cooling costs but also significantly decreases the overall carbon footprint of the facility. Moreover, the improved thermal insulation provided by these windows helps maintain a consistent and comfortable indoor climate, which is beneficial for the learning environment. Additionally, the use of low-emissivity coatings on these windows can block up to 99% of UV radiation, protecting interior furnishings from sun damage and further contributing to the sustainability efforts of the school. Overall, the adoption of high-performance windows is a cost-effective measure that aligns with modern energy standards and environmental stewardship, making it a prudent investment for educational institutions aiming to modernize their facilities and reduce operational costs."))
        ######
        self.Action_Increase_Office_AC_1C = QRadioButton("Increase all office ACs by 1C")
        self.Action_Increase_Office_AC_1C.toggled.connect(partial(self.update_action_information,
                                                                       f"According to information from the property management, the majority of the spaces within the school are offices, not classrooms. By increasing the temperature setting on all office air conditioners by one degree Celsius, we can achieve a substantial reduction in the school's total energy usage. This specific adjustment is an effective way to decrease energy consumption and associated costs.\n\n" 
                                                                       f"No cost required!"))
        ######
        self.Action_Increase_Classroom_AC_1C = QRadioButton("Increase all classroom ACs by 1C")
        self.Action_Increase_Classroom_AC_1C.toggled.connect(partial(self.update_action_information,
                                                                     f"Increasing the temperature of air conditioners in classrooms by 1°C can reduce energy consumption and associated carbon emissions. This is because air conditioning systems consume less energy when set at a slightly higher temperature, leading to lower electricity usage. Since much of the electricity is still generated from fossil fuels, reducing energy consumption also decreases carbon emissions, aiding in the fight against climate change.\n\n"
                                                                     f"No cost required!"))

        self.main_UI_setup()

    def main_UI_setup(self):
        # TIMER
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # TITLE
        self.setWindowTitle("Green Campus Simulator [[DEMO]]")
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.showMaximized()
        self.setFixedSize(self.size())
        ######
        self.general_font = QFont("Helvetica", 20)
        self.general_font.setBold(True)
        self.important_log_font = QFont("Helvetica", 15)
        self.important_log_font.setBold(True)
        ######
        self.game_author = QLabel(f"By REN Yixiao & YANG Xikun")
        self.game_author.setFont(self.general_font)
        self.game_author.setAlignment(Qt.AlignCenter)
        ######
        self.game_time = QLabel("Game not started")
        self.game_time.setFont(self.general_font)
        self.game_time.setAlignment(Qt.AlignCenter)
        ######
        self.game_budget = QLabel("Game not started")
        self.game_budget.setFont(self.general_font)
        self.game_budget.setAlignment(Qt.AlignCenter)

        # MAIN VBOXLAYOUT
        self.main_v_layout = QVBoxLayout()

        # PHOTO LAYOUT
        self.game_status_h_layout = QHBoxLayout()
        self.map_and_curve_h_box = QHBoxLayout()
        self.actions_h_box = QHBoxLayout()

        # TIMER BUTTON
        self.game_status_toggling_button = QPushButton("🎮  Start Game  🎮")
        self.game_status_toggling_button.setFont(self.general_font)
        self.game_status_toggling_button.clicked.connect(self.toggle_game_status)

        # FINALIZED GAME STATUS H_BOX ADDING WIDGETS
        self.game_status_h_layout.addWidget(self.game_author)
        self.game_status_h_layout.addWidget(self.game_time)
        self.game_status_h_layout.addWidget(self.game_budget)
        self.game_status_h_layout.addWidget(self.game_status_toggling_button)

        # MAP
        self.campus_map = Image_Template("PolyU_Map_Main.png", fixed_height=self.map_and_curve_maximum_height)

        # CURVE
        self.carbon_emission_figure = Figure_Template(self, width=5, height=3, dpi=100)
        self.carbon_emission_figure.axes.set_title('PolyU Carbon Emission Curve')
        self.carbon_emission_figure.axes.set_xlabel('Time (month)')
        self.carbon_emission_figure.axes.set_ylabel('Relative Carbon Emission (%)')
        self.carbon_emission_figure_line, = self.carbon_emission_figure.axes.plot(self.carbon_emission_time_series,
                                                                                  self.carbon_emission_data, color = "black")
        self.carbon_emission_figure.axes.set_xlim(0, self.max_game_time)
        self.carbon_emission_figure.axes.set_ylim(0, 100 + 20)
        self.carbon_emission_figure.setMaximumHeight(self.map_and_curve_maximum_height)

        # FINALIZED MAP AND CURVE H_BOX ADDING WIDGETS
        self.map_and_curve_h_box.addWidget(self.campus_map, 1)
        self.map_and_curve_h_box.addWidget(self.carbon_emission_figure, 2)

        # FINALIZED ACTIONS H_BOX ADDING WIDGETS
        self.actions_log_v_box = QVBoxLayout()
        self.actions_log_title = QLabel("Log")
        self.actions_log_title.setFont(self.general_font)
        self.actions_log = QListWidget_New()
        self.actions_log.setWordWrap(True)
        self.game_starter_log = QListWidgetItem(f"== Game to start == \n\n"
                                                f"You are a school manager, and now you have {self.max_game_time / 12}yrs term.\n\n"
                                                f"During your office term, try your best to REDUCE THE CARBON EMISSION on campus as much as possible.")
        self.game_starter_log.setFont(self.important_log_font)
        self.actions_log.insertItem(0, self.game_starter_log)
        self.actions_log.insertItem(0, "")
        self.actions_log_v_box.addWidget(self.actions_log_title)
        self.actions_log_v_box.addWidget(self.actions_log)
        ######
        self.infrastructure_actions_v_box = QVBoxLayout()
        self.infrastructure_actions_title = QLabel("Infrastructure Actions")
        self.infrastructure_actions_title.setFont(self.general_font)
        self.infrastructure_actions_v_box_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.infrastructure_actions_v_box.addWidget(self.infrastructure_actions_title)
        self.infrastructure_actions_v_box.addWidget(self.Action_Plant_Plants_Near_Car_Road)
        self.infrastructure_actions_v_box.addWidget(self.Action_Build_Carpark)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Reflective_Insulation_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Nano_Ceramic_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Phase_Change_Material)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Silicate_Insulation_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Hollow_Glass_Microsphere_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Vacuum_Insulation_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Polyurethane_Foam_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Infrared_Reflective_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Florocarbon_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Graphene_Insulation_Coating)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Solar_Panels_Minor)
        self.infrastructure_actions_v_box.addWidget(self.Action_Use_Solar_Panels_Major)
        self.infrastructure_actions_v_box.addWidget(self.Action_Arrange_More_Effective_LED)
        self.infrastructure_actions_v_box.addWidget(self.Action_Arrange_Smart_Thermostats)
        self.infrastructure_actions_v_box.addWidget(self.Action_Arrange_High_Performance_Windows)
        self.infrastructure_actions_v_box.addItem(self.infrastructure_actions_v_box_spacer)
        ######
        self.carbon_reducing_actions_v_box = QVBoxLayout()
        self.carbon_reducing_actions_title = QLabel("Carbon Reducing Actions")
        self.carbon_reducing_actions_title.setFont(self.general_font)
        self.carbon_reducing_actions_v_box_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.carbon_reducing_actions_v_box.addWidget(self.carbon_reducing_actions_title)
        self.carbon_reducing_actions_v_box.addWidget(self.Action_Increase_Office_AC_1C)
        self.carbon_reducing_actions_v_box.addWidget(self.Action_Increase_Classroom_AC_1C)
        self.carbon_reducing_actions_v_box.addItem(self.carbon_reducing_actions_v_box_spacer)
        ######
        self.action_information_textbox_label = QLabel("Action Information")
        self.action_information_textbox_label.setFont(self.general_font)
        self.information_and_action_v_box = QVBoxLayout()
        self.action_information_textbox = QTextEdit(self)
        self.action_information_textbox.setText(f"")
        self.action_information_textbox.setReadOnly(True)
        self.act_button = QPushButton("🚀  Act your operation  🚀")
        self.act_button.clicked.connect(self.act_main)
        self.act_button.setFont(self.general_font)
        self.act_button.setEnabled(False)
        self.information_and_action_v_box.addWidget(self.action_information_textbox_label)
        self.information_and_action_v_box.addWidget(self.action_information_textbox)
        self.information_and_action_v_box.addWidget(self.act_button)

        ######
        self.actions_h_box.addLayout(self.actions_log_v_box, 5)
        self.actions_h_box.addLayout(self.infrastructure_actions_v_box, 5)
        self.actions_h_box.addLayout(self.carbon_reducing_actions_v_box, 5)
        self.actions_h_box.addLayout(self.information_and_action_v_box, 7)

        # FINALIZED V_BOX ADDING LAYOUTS
        self.main_v_layout.addLayout(self.game_status_h_layout)
        self.main_v_layout.addLayout(self.map_and_curve_h_box)
        self.main_v_layout.addLayout(self.actions_h_box)

        # SET VBOXLAYOUT
        self.setLayout(self.main_v_layout)

    def update_timer(self):
        self.current_game_time += 1
        self.game_budget_count += self.monthly_invest
        ######
        self.carbon_emission_time_series.append(self.current_game_time)
        ######
        new_carbon_emission_data = sum(action.carbon_reducing for action in self.ongoing_actions if action.starting_month == self.current_game_time)
        self.carbon_emission_data.append(self.carbon_emission_data[-1] - new_carbon_emission_data if len(self.carbon_emission_data) > 0 else 100)
        ######
        self.carbon_emission_figure_line.set_xdata(self.carbon_emission_time_series)
        self.carbon_emission_figure_line.set_ydata(self.carbon_emission_data)
        self.carbon_emission_figure.axes.relim()
        self.carbon_emission_figure.axes.autoscale_view()
        self.carbon_emission_figure.draw()
        ######
        self.game_budget.setText(f"Budget: $$ {self.game_budget_count}")
        self.act_button.setEnabled(True)

        if self.current_game_time == 1:
            self.game_time.setText(f"Time: {self.current_game_time} month,  {self.max_game_time - self.current_game_time} months left")
        elif self.current_game_time == self.max_game_time + 1 or self.carbon_emission_data[-1] <= 0:
            game_over = True
            self.game_over_main()
        else:
            if self.max_game_time - self.current_game_time == 1:
                self.game_time.setText(f"Time: {self.current_game_time} month,  {self.max_game_time - self.current_game_time} month left")
            else:
                self.game_time.setText(f"Time: {self.current_game_time} month,  {self.max_game_time - self.current_game_time} months left")

    def toggle_game_status(self):
        self.game_started = not self.game_started
        if not self.game_started:
            self.timer.stop()
            self.game_status_toggling_button.setText("🎮  Resume Game  🎮")
        else:
            self.timer.start(2000)
            self.game_status_toggling_button.setText("⏸️  Pause Game  ⏸️")

    def act_main(self):
        new_ongoing_action = Action("DEFAULT", self.current_game_time, self.current_game_time + 1, 0, 0)
        no_enough_budget = False
        empty_action = True

        if self.Action_Increase_Office_AC_1C.isEnabled() and self.Action_Increase_Office_AC_1C.isChecked():
            empty_action = False
            new_ongoing_action.name = "Increase all office ACs by 1C"
            new_ongoing_action.carbon_reducing = 3
            if self.game_budget_count >= new_ongoing_action.cost:
                self.Action_Increase_Office_AC_1C.setEnabled(False)
            else:
                no_enough_budget = True
        elif self.Action_Increase_Classroom_AC_1C.isEnabled() and self.Action_Increase_Classroom_AC_1C.isChecked():
            empty_action = False
            new_ongoing_action.name = "Increase all classroom ACs by 1C"
            new_ongoing_action.carbon_reducing = 1
            if self.game_budget_count >= new_ongoing_action.cost:
                self.Action_Increase_Classroom_AC_1C.setEnabled(False)
            else:
                no_enough_budget = True
        elif self.Action_Plant_Plants_Near_Car_Road.isEnabled() and self.Action_Plant_Plants_Near_Car_Road.isChecked():
            empty_action = False
            new_ongoing_action.name = "Plant plants near car road"
            new_ongoing_action.starting_month = self.current_game_time + 3
            new_ongoing_action.cost = 10
            new_ongoing_action.carbon_reducing = 1
            if self.game_budget_count >= new_ongoing_action.cost:
                self.Action_Plant_Plants_Near_Car_Road.setEnabled(False)
            else:
                no_enough_budget = True
        elif self.Action_Build_Carpark.isEnabled() and self.Action_Build_Carpark.isChecked():
            empty_action = False
            new_ongoing_action.name = "Build carpark"
            new_ongoing_action.starting_month = self.current_game_time + 3
            new_ongoing_action.cost = 20
            new_ongoing_action.carbon_reducing = 1
            if self.game_budget_count >= new_ongoing_action.cost:
                self.Action_Build_Carpark.setEnabled(False)
                self.ongoing_actions.append(Action("CARPARK_CONSTRUCTION_SITE", self.current_game_time, self.current_game_time + 1, 0, -2))
            else:
                no_enough_budget = True

        if empty_action:
            self.actions_log.insertItem(0, f"Empty action")
        elif self.game_budget_count >= new_ongoing_action.cost:
            self.actions_log.insertItem(0, f"Month {new_ongoing_action.implement_month}, action: {new_ongoing_action.name}, cost $$ {new_ongoing_action.cost}")
            self.game_budget_count -= new_ongoing_action.cost
            self.ongoing_actions.append(new_ongoing_action)
            self.game_budget.setText(f"Budget: $$ {self.game_budget_count}")
        elif no_enough_budget:
            self.actions_log.insertItem(0, f"No enough budget for action: {new_ongoing_action.name}")
            self.act_button.setEnabled(False)

    def update_action_information(self, information_detail):
        self.action_information_textbox.setText(information_detail)

    def game_over_main(self):
        self.timer.stop()
        self.game_status_toggling_button.setText("✅  The game is over!  ✅")
        self.game_status_toggling_button.setEnabled(False)
        return


if __name__ == "__main__":
    GreenCampusSimulator = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(GreenCampusSimulator.exec_())
