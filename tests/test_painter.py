import random
from unittest import TestCase, main
from data_base import class_db
import os
from pathlib import *

__current_dir = str(Path.cwd())
print(__current_dir)
__name_db = 'test'
db_name, db_path = class_db.Data_base('', '').db_create()
#
# class PainterTest(TestCase):
#
#
#     ...
#         # __current_dir = Path.cwd()
#         # __name_db = 'test'
#         # class_db.Data_base('','').db_create(name_db=__name_db, path_db=__current_dir, status=True)
#         # self.assertEqual(('__current_dir',f'{__name_db}.db'), class_db.Data_base('','').db_create(name_db=__name_db, path_db=__current_dir, status=True))
#     # def test_strait_fire_greater_than_zero(self):
#     #     for _ in range(1, 5):
#     #         s = random.randint(20, 50)
#     #         v = random.choice((1, 2, 3, 4, 5))
#     #         self.assertGreater(
#     #             round(calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=s, m_sg=0.06, mol_mass=95,
#     #                                                                         t_boiling=68, wind_velocity=v, radius=40),
#     #                   1),
#     #             0)
#     #
#     # def test_strait_fire_lpg(self):
#     #     self.assertEqual(
#     #         round(calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=20, m_sg=0.1, mol_mass=44,
#     #                                                                     t_boiling=-15, wind_velocity=1, radius=50), 1),
#     #         0.8)
#     #
#     # def test_strait_fire_with_null_param(self):
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=0, m_sg=0.1, mol_mass=44,
#     #                                                               t_boiling=0, wind_velocity=1, radius=50)
#     #
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=20, m_sg=0, mol_mass=0,
#     #                                                               t_boiling=200, wind_velocity=0, radius=50)
#     #
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     # def test_count_array_result(self):
#     #     for s in range(20, 200, 25):
#     #         v = random.choice((1, 2, 3, 4, 5))
#     #         self.assertEqual(len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.1, mol_mass=44,
#     #                                                                                    t_boiling=-15, wind_velocity=v)[
#     #                                  0]),
#     #                          len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.1, mol_mass=44,
#     #                                                                                    t_boiling=-15, wind_velocity=v)[
#     #                                  1]))
#     #
#     #         self.assertEqual(
#     #             len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.3, mol_mass=144,
#     #                                                                       t_boiling=-10, wind_velocity=v)[2]),
#     #             len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.3, mol_mass=144,
#     #                                                                       t_boiling=-10, wind_velocity=v)[3]))
#     #     # END
#     #
#     # # START 2. Тестирование пробит-функции
#     #
#     # def test_probit_check(self):
#     #     self.assertEqual(calc_probit.Probit().probit_check(probit=11), 8.09)
#     #     self.assertEqual(calc_probit.Probit().probit_check(probit=2), 0)
#     #     self.assertEqual(calc_probit.Probit().probit_check(probit=3.33), 3.33)
#     #
#     # def test_probability(self):
#     #     self.assertEqual(calc_probit.Probit().probability(probit=8.99), 0.99)
#     #     self.assertEqual(calc_probit.Probit().probability(probit=-12), 0)
#     #     self.assertEqual(round(calc_probit.Probit().probability(probit=3.35), 2), 0.05)
#     #
#     # def test_probit_explosion_with_null_param(self):
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_probit.Probit().probit_explosion(delta_P=0, impuls=161)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_probit.Probit().probit_explosion(delta_P=0, impuls=0)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     # def test_probit_fireball_with_null_param(self):
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_probit.Probit().probit_fireball(time=0, q_ball=125)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_probit.Probit().probit_fireball(time=0, q_ball=0)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     # def test_probit_strait_fire_with_null_param(self):
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_probit.Probit().probit_strait_fire(dist=0, q_max=0)
#     #     self.assertEqual('math domain error', e.exception.args[0])
#     #
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_probit.Probit().probit_strait_fire(dist=10, q_max=0)
#     #     self.assertEqual('math domain error', e.exception.args[0])
#     #
#     # # END
#     #
#     # # START 3. Тестирование взрыва (СП 12.13130-2009)
#     # def test_explosion_point(self):
#     #     self.assertEqual(
#     #         round(
#     #             calc_sp_explosion.Explosion().explosion_point(mass=254400, heat_of_combustion=46000, z=0.1, radius=500)[
#     #                 0], 2), 15.5)
#     #
#     # def test_explosion_point_greater_than_zero(self):
#     #     for m in range(100, 1000, 250):
#     #         h = random.randint(46000, 101000)
#     #         z = random.choice((0.1, 0.3, 0.5))
#     #         r = random.randint(10, 60)
#     #         self.assertGreater(
#     #             round(
#     #                 calc_sp_explosion.Explosion().explosion_point(mass=m, heat_of_combustion=h, z=z,
#     #                                                               radius=r)[0], 1), 0)
#     #
#     # def test_explosion_with_null_param(self):
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_sp_explosion.Explosion().explosion_point(mass=0, heat_of_combustion=101000, z=0.1, radius=50)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_sp_explosion.Explosion().explosion_point(mass=0, heat_of_combustion=0, z=0.1, radius=0)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     # def test_count_array_result_explosion(self):
#     #     for m in range(100, 1000, 250):
#     #         h = random.randint(46000, 101000)
#     #         z = random.choice((0.1, 0.3, 0.5))
#     #
#     #         self.assertEqual(
#     #             len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=h, z=z)[0]),
#     #             len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=h, z=z)[1]))
#     #
#     #         self.assertEqual(
#     #             len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=h, z=z)[2]),
#     #             len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=h, z=z)[3]))
#     #     # END
#     #
#     # # END
#     #
#     # # START 4. Тестирование взрыва (ТВС методика)
#     # def test_v_burn_point(self):
#     #     tmp = (500, 500, 300, 200)
#     #     for view in range(1, 5):
#     #         self.assertEqual(calc_tvs_explosion.Explosion().burn_rate(class_substance=1, view_space=view, mass=200),
#     #                          tmp[view - 1])
#     #
#     #     tmp = (500, 300, 200, 150)
#     #     for view in range(1, 5):
#     #         self.assertEqual(calc_tvs_explosion.Explosion().burn_rate(class_substance=2, view_space=view, mass=200),
#     #                          tmp[view - 1])
#     #     mass = 2000
#     #     tmp = (300, 200, 150, 43 * pow(mass, 1 / 6))
#     #     for view in range(1, 5):
#     #         self.assertEqual(calc_tvs_explosion.Explosion().burn_rate(class_substance=3, view_space=view, mass=mass),
#     #                          tmp[view - 1])
#     #
#     #     mass = 2000
#     #     tmp = (200, 150, 43 * pow(mass, 1 / 6), 26 * pow(mass, 1 / 6))
#     #     for view in range(1, 5):
#     #         self.assertEqual(calc_tvs_explosion.Explosion().burn_rate(class_substance=4, view_space=view, mass=mass),
#     #                          tmp[view - 1])
#     #
#     # def test_explosion_tvs_point(self):
#     #     self.assertEqual(
#     #         round(
#     #             calc_tvs_explosion.Explosion().explosion_point(class_substance=1, view_space=2,
#     #                                                            mass=2000, heat_of_combustion=46000, sigma=7,
#     #                                                            energy_level=2, radius=200)[
#     #                 0], 2), 85.3)
#     #
#     # def test_explosion_tvs_point_greater_than_zero(self):
#     #     for m in range(100, 1000, 250):
#     #         c = random.randint(1, 4)
#     #         v = random.randint(1, 4)
#     #         e = random.randint(1, 2)
#     #         r = random.randint(10, 50)
#     #         self.assertGreater(
#     #             round(calc_tvs_explosion.Explosion().explosion_point(class_substance=c,
#     #                                                                  view_space=v, mass=m,
#     #                                                                  heat_of_combustion=46000, sigma=7,
#     #                                                                  energy_level=e,
#     #                                                                  radius=r)[0], 1), 0)
#     #
#     # def test_explosion_tvs_with_null_param(self):
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_tvs_explosion.Explosion().explosion_point(class_substance=10,
#     #                                                        view_space=1, mass=0,
#     #                                                        heat_of_combustion=0, sigma=7,
#     #                                                        energy_level=2,
#     #                                                        radius=10)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_tvs_explosion.Explosion().explosion_point(class_substance=0,
#     #                                                        view_space=1, mass=0,
#     #                                                        heat_of_combustion=0, sigma=7,
#     #                                                        energy_level=10,
#     #                                                        radius=0)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     # def test_count_array_result_explosion_tvs(self):
#     #     for m in range(10, 100, 25):
#     #         self.assertEqual(
#     #             len(calc_tvs_explosion.Explosion().explosion_array(class_substance=1, view_space=1, mass=m,
#     #                                                                heat_of_combustion=46000, sigma=7, energy_level=2)[
#     #                     0]),
#     #             len(calc_tvs_explosion.Explosion().explosion_array(class_substance=1, view_space=1, mass=m,
#     #                                                                heat_of_combustion=46000, sigma=7, energy_level=2)[
#     #                     1]))
#     #
#     #         self.assertEqual(
#     #             len(calc_tvs_explosion.Explosion().explosion_array(class_substance=1, view_space=1, mass=m,
#     #                                                                heat_of_combustion=46000, sigma=7, energy_level=2)[
#     #                     2]),
#     #             len(calc_tvs_explosion.Explosion().explosion_array(class_substance=1, view_space=1, mass=m,
#     #                                                                heat_of_combustion=46000, sigma=7, energy_level=2)[
#     #                     3]))
#     #
#     # # END
#     #
#     # # START 5. Тестирование огненного шара
#     # def test_fireball_point(self):
#     #     self.assertEqual(
#     #         round(calc_fireball.Fireball().fireball_point(mass=2.54 * pow(10, 5), ef=450, radius=500)[0], 2), 12.9)
#     #
#     # def test_fireball_greater_than_zero(self):
#     #     for m in range(100, 1000, 250):
#     #         e = random.choice((350, 450))
#     #         r = random.randint(100, 200)
#     #         self.assertGreater(round(calc_fireball.Fireball().fireball_point(mass=m, ef=e, radius=r)[0], 1), 0)
#     #
#     # def test_fireball_with_null_param(self):
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_fireball.Fireball().fireball_point(mass=0, ef=0, radius=0)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     #     with self.assertRaises(ValueError) as e:
#     #         calc_fireball.Fireball().fireball_point(mass=0, ef=450, radius=10)
#     #     self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])
#     #
#     # def test_fireball_explosion_tvs(self):
#     #     for m in range(1000, 10000, 250):
#     #         self.assertEqual(len(calc_fireball.Fireball().fireball_array(mass=m, ef=450)[0]),
#     #                          len(calc_fireball.Fireball().fireball_array(mass=m, ef=450)[1]))
#     #
#     #         self.assertEqual(len(calc_fireball.Fireball().fireball_array(mass=m, ef=450)[2]),
#     #                          len(calc_fireball.Fireball().fireball_array(mass=m, ef=450)[3]))
#     #
#     # # END
#     #
#     # # START 5. Тестирование НКПР и пожара-вспышки
#     # def test_lclp(self):
#     #     self.assertEqual(
#     #         round(calc_lower_concentration.LCLP().lower_concentration_limit(mass=200, mol_mass=100, t_boiling=63,
#     #                                                                         lower_concentration=1.8)[0], 2), 24.14)
#     #
#     # def test_lclp_greater_than_zero(self):
#     #     for m in range(100, 1000, 250):
#     #         t = random.choice((10, 100))
#     #         l = random.randint(1, 10)
#     #         self.assertGreater(
#     #             round(calc_lower_concentration.LCLP().lower_concentration_limit(mass=m, mol_mass=100, t_boiling=t,
#     #                                                                             lower_concentration=l)[0], 1), 0)
#     #
#     # # END
#
#
# if __name__ == '__main__':
#     main()
